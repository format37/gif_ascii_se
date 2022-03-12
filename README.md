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
python3 gif-to-ascii.py 80 10 100000 0
```
Where  
- 80 is cols count (size)  
- 10 is down-step  
- 100000 is script lenght limit  
- 0 is morelevels parameter (1 to enable)  
4. check the selected animation
```
cd cs
./compile.sh fraksl-fractals.cs
```
4. press ctrl+c to stop infinity loop
5. copy source code of se/your_script.cs and paste them to space engioneers program block. Don't foirget to set name of lcd
