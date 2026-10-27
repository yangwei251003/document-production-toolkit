import json,os,subprocess,sys,tempfile,unittest,zipfile
from pathlib import Path
from document_toolkit.__main__ import ROOT
from document_toolkit.session_demo import reader_functions

class SessionToolTests(unittest.TestCase):
    def test_original_workbook_flow_generates_two_synthetic_variants(self):
        with tempfile.TemporaryDirectory() as tmp:
            output=Path(tmp)/'new-output'
            p=subprocess.run([sys.executable,'-m','document_toolkit.session_demo','--output',str(output)],cwd=ROOT,capture_output=True)
            self.assertEqual(p.returncode,0,p.stderr.decode(errors='replace'))
            result=json.loads((output/'session-result.json').read_text(encoding='utf-8'))
            self.assertEqual(len(result['workbooks']),2)
            self.assertEqual(sum(len(x['sheets']) for x in result['workbooks']),8)
            self.assertFalse(result['original_io_executed']);self.assertFalse(result['office_executed'])
            for book in result['workbooks']:
                for sheet in book['sheets']:
                    self.assertGreater(sheet['rows'],1);self.assertTrue(sheet['freeze_panes']);self.assertTrue(sheet['styled_header'])
                with zipfile.ZipFile(output/book['file']) as package:self.assertIn('xl/workbook.xml',package.namelist())
            snapshot=(output/'session-result.json').read_bytes()
            p=subprocess.run([sys.executable,'-m','document_toolkit.session_demo','--output',str(output)],cwd=ROOT,capture_output=True)
            self.assertNotEqual(p.returncode,0);self.assertEqual(snapshot,(output/'session-result.json').read_bytes())

    def test_original_reader_helpers_format_and_escape_synthetic_input(self):
        helpers=reader_functions()
        out=helpers['md_to_html']('# Synthetic heading\n\n**Synthetic emphasis**\n\n- Synthetic item\n')
        self.assertIn('<h1',out);self.assertIn('<strong>',out);self.assertIn('<li>',out)
        self.assertNotIn('<script>',helpers['md_inline']('<script>example</script>'))
        self.assertIn('<table',helpers['md_to_html']('| A | B |\n| --- | --- |\n| Synthetic A | Synthetic B |'))
        self.assertIsInstance(helpers['human_size'](1024),str)

    def test_session_office_signature_and_original_reader_io_are_blocked(self):
        paths=['session/2026-09-15-10-34-50/_work/make_signature3.py','session/2026-09-08-23-38-21/setup_print.py','session/2026-10-04-22-46-18/build_reader.py','session/2026-10-07-21-33-31/.参赛信息表.ref/build.py']
        with tempfile.TemporaryDirectory() as tmp:
            for rel in paths:
                p=subprocess.run([sys.executable,str(ROOT/'archive'/rel)],cwd=tmp,env={**os.environ,'PYTHONPATH':str(ROOT)},capture_output=True)
                self.assertNotEqual(p.returncode,0);self.assertIn(b'disabled by default',p.stderr)
            self.assertEqual(list(Path(tmp).iterdir()),[])

if __name__=='__main__':unittest.main()
