cd wbia_curvrank_v2/
make -f MakefileAStar
make -f MakefileDTW
cd ../
python setup.py build_ext --inplace
pip install -e .
