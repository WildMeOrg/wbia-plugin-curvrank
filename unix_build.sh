cd src/
make -f MakefileAStar
cp -v astar.so ../ibeis_curvrank
make -f MakefileDTW
cp -v dtw.so ../ibeis_curvrank
cd ../
pip install -e .
