set term x11 size 800,600
set datafile separator ","
set multiplot title "AQI Recorder"
set tmargin 0.05
set bmargin 0
set size 0.94,0.1
set origin 0.03,0.85
unset xtics
set ytics nomirror format "%5.0f"
plot '< tail -n 600 aqi.dat' using 0:14 w line t "PM0.3 Count"
set tmargin 0
set size 0.94,0.1
set origin 0.03,0.75
plot '< tail -n 600 aqi.dat' using 0:15 w line t "PM0.5 Count"
set size 0.94,0.1
set origin 0.03,0.65
plot '< tail -n 600 aqi.dat' using 0:16 w line t "PM1.0 Count"
set size 0.94,0.1
set origin 0.03,0.55
plot '< tail -n 600 aqi.dat' using 0:17 w line t "PM2.5 Count"
set size 0.94,0.1
set origin 0.03,0.45
plot '< tail -n 600 aqi.dat' using 0:18 w line t "PM5.0 Count"
set size 0.94,0.1
set origin 0.03,0.35
plot '< tail -n 600 aqi.dat' using 0:19 w line t "PM10 Count"
set tmargin 0
set size 0.94,0.25
set origin 0.03,0.1
set xtics nomirror rotate 90 scale 0
plot '< tail -n 600 aqi.dat' using 0:3:xticlabel(int($0)%30 == 0 ?strcol(2):'') w line t "AQI"
unset multiplot
pause 10
reread
