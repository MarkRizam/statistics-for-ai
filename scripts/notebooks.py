"""Execute clean source notebooks in fresh kernels; save status, not bulky output."""
from pathlib import Path
import json
import nbformat
from nbclient import NotebookClient

root=Path(__file__).resolve().parents[1]
if __name__=='__main__':
    status=[]
    for path in sorted((root/'notebooks').glob('*.ipynb')):
        nb=nbformat.read(path,as_version=4)
        NotebookClient(nb,timeout=120,kernel_name='python3',resources={'metadata':{'path':str(root)}}).execute()
        status.append({'notebook':path.name,'status':'pass','executed_code_cells':sum(c.cell_type=='code' for c in nb.cells)})
        print(path.name,'PASS',flush=True)
    assert len(status)==8
    (root/'results'/'notebook-status.json').write_text(json.dumps(status,indent=2)+'\n')
