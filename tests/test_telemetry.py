"""Data-integrity and failure-preservation checks; no network or synthetic profile output."""
from datetime import datetime, timezone
from pathlib import Path
import sys
import tempfile
import unittest
from urllib.error import HTTPError
import xml.etree.ElementTree as ET

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import generate_telemetry as telemetry

NOW=datetime(2026,9,14,tzinfo=timezone.utc)


def repo(name='Example',**kwargs):
    return dict(name=name,owner={'login':telemetry.OWNER},fork=False,archived=False,private=False,disabled=False,size=20,language='Python',pushed_at='2026-09-13T12:00:00Z') | kwargs


class TelemetryTests(unittest.TestCase):
    def test_scope_and_dates(self):
        rows=[repo(),repo('Old',pushed_at='2026-01-01T00:00:00Z',language=None),repo('Boundary',pushed_at='2026-06-16T00:00:00Z'),repo('Foreign',owner={'login':'elsewhere'}),repo(telemetry.OWNER),repo('Fork',fork=True),repo('Archived',archived=True),repo('Private',private=True),repo('Empty',size=0),repo('Disabled',disabled=True)]
        data=telemetry.snapshot(rows,NOW)
        self.assertEqual(data['public_project_count'],3)
        self.assertEqual(data['recently_pushed_count'],2)
        self.assertEqual(data['primary_languages'],['Python'])
        self.assertEqual(data['recent_projects'][0]['name'],'Example')

    def test_pagination_and_duplicate_detection(self):
        rows=[repo('Repo'+str(n)) for n in range(101)]
        self.assertEqual(len(telemetry.fetch_repositories(lambda page:rows[(page-1)*100:page*100])),101)
        with self.assertRaises(ValueError):telemetry.fetch_repositories(lambda page:rows[:100] if page==1 else [rows[0]])

    def test_missing_metadata_fails_closed(self):
        broken=repo();del broken['private']
        with self.assertRaises(ValueError):telemetry.snapshot([broken],NOW)
        with self.assertRaises(ValueError):telemetry.fetch_repositories(lambda page:{'message':'API error'})
        with self.assertRaises(ValueError):telemetry.snapshot([repo(pushed_at='2027-01-01T00:00:00Z')],NOW)

    def test_api_failure_keeps_all_prior_files(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);(root/'README.md').write_text(telemetry.START+'old'+telemetry.END)
            old=root/'assets/generated/telemetry.svg';old.parent.mkdir(parents=True);old.write_text('prior-image')
            def fail(page):raise HTTPError('https://api.github.com',403,'rate limited',{},None)
            with self.assertRaises(HTTPError):telemetry.refresh(root,fail,NOW)
            self.assertEqual(old.read_text(),'prior-image')
            self.assertIn('old',(root/'README.md').read_text())
            self.assertEqual(len(list(root.rglob('*.*'))),2)

    def test_partial_pagination_and_missing_markers_do_not_write(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);original='No marker pair';(root/'README.md').write_text(original)
            with self.assertRaises(ValueError):telemetry.refresh(root,lambda page:[repo()],NOW)
            self.assertEqual((root/'README.md').read_text(),original)
            def partial(page):
                if page==1:return [repo('Repo'+str(n)) for n in range(100)]
                raise HTTPError('https://api.github.com',502,'unavailable',{},None)
            with self.assertRaises(HTTPError):telemetry.refresh(root,partial,NOW)
            self.assertEqual(list(root.iterdir()),[root/'README.md'])

    def test_rendering_escapes_data_and_preserves_other_readme_sections(self):
        data=telemetry.snapshot([repo(language='<untrusted>&')],NOW)
        outputs=telemetry.prepare_outputs(data,'BEFORE'+telemetry.START+'old'+telemetry.END+'AFTER')
        self.assertTrue(outputs['README.md'].startswith('BEFORE'))
        self.assertTrue(outputs['README.md'].endswith('AFTER'))
        for name,content in outputs.items():
            if name.endswith('.svg'):
                root=ET.fromstring(content)
                self.assertEqual(root.tag,'{http://www.w3.org/2000/svg}svg')
                self.assertNotIn('<untrusted>',content)
        self.assertEqual(len(outputs),6)

    def test_no_language_or_push_data_is_not_invented(self):
        data=telemetry.snapshot([repo(language=None,pushed_at=None)],NOW)
        self.assertEqual(data['public_project_count'],1)
        self.assertEqual(data['recently_pushed_count'],0)
        self.assertEqual(data['recent_projects'],[])
        self.assertIn('not reported',telemetry.markdown(data))
        self.assertIn('No push dates reported',telemetry.render_svg(data))

if __name__=='__main__':unittest.main()
