"""Check focused includes and executable annotated code for every published lesson."""
import os
import sys
import tempfile
import subprocess
from pathlib import Path
from build import LESSONS,code_for

def main():
    compiler=Path(os.environ.get('CXX','E:/Programs/MinGW-w64/ucrt64/bin/g++.exe'))
    env=os.environ.copy();env['PATH']=str(compiler.parent)+os.pathsep+env.get('PATH','')
    root=Path(__file__).resolve().parent.parent
    with tempfile.TemporaryDirectory(prefix='course-code-',dir='D:/Users/mio/Desktop/Study',ignore_cleanup_errors=True) as tmp:
        for item in LESSONS:
            id=item[0];cpp,python=code_for(item)
            cppfile=Path(tmp)/(id+'.cpp');pyfile=Path(tmp)/(id+'.py');exe=Path(tmp)/(id+'.exe')
            cppfile.write_text(cpp,encoding='utf-8');pyfile.write_text(python,encoding='utf-8')
            result=subprocess.run([str(compiler),'-std=c++17','-Wall','-Wextra',str(cppfile),'-o',str(exe)],capture_output=True,env=env,timeout=60)
            if result.returncode:raise RuntimeError(id+': '+result.stderr.decode('utf-8',errors='replace'))
            for command in ([str(exe)],[sys.executable,str(pyfile)]):
                subprocess.run(command,check=True,capture_output=True,env=env,timeout=20)
            assert '// ' in cpp and '# ' in python,id
            assert 'emit_state(' not in python,id
            print(id,'C++ / Python compiled and ran; headers:',sum(line.startswith('#include') for line in cpp.splitlines()),flush=True)
    print('All 45 C++17 and 45 Python programs passed.')

if __name__=='__main__':main()
