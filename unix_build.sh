cd src/
make -f MakefileAStar
cp -v astar.so ../ibeis_curverank
make -f MakefileDTW
cp -v dtw.so ../ibeis_curverank
cd ../
