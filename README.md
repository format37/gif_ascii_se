# gif_ascii_se
git to ascii animation for space engineers game  
### install
```
git clone https://github.com/format37/gif_ascii_se.git
cd gif_ascii_se
sudo apt-get install mono-complete
```
### use
1. put 1 or several gif animation files to gifs path  
2. run
```
python3 gif-to-ascii.py 80 10
```
Where 80 is cols count (size), and 10 is down-step  
3. check the selected animation
```
cd cs
mcs -out:film.exe fraksl-fractals.cs
mono film.exe
```
4. press ctrl+c to stop infinity loop
5. copy source code of se/your_script.cs and paste them to space engioneers program block. Don't foirget to set name or lcd
