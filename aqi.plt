set xtics nomirror
set xtics rotate 90
set xtics scale 0
plot '< tail -n 60 aqi.dat' using 0:3:xticlabel(int($0)%10 == 0 ?strcol(2):'') w line t "AQI"
pause 3
reread
