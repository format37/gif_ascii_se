import sys
import os
#import argparse
#import math
#import random
import numpy as np
from PIL import Image

# 70 levels of gray
gscale1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

# 10 levels of gray
gscale2 = '@%#*+=-:. '


def getAverageL(image):
    """
    Given PIL Image, return average value of grayscale value
    """
    # get image as numpy array
    im = np.array(image)
    # get shape
    w, h = im.shape
    # get average
    return np.average(im.reshape(w * h))


def covertImageToAscii(image, cols, scale, moreLevels):
    """
    Given Image and dims (rows, cols) returns an m*n list of Images
    """
    # declare globals
    global gscale1, gscale2
    # store dimensions
    W, H = image.size[0], image.size[1]
    # compute width of tile
    w = W / cols
    # compute tile height based on aspect ratio and scale
    h = w / scale
    # compute number of rows
    rows = int(H / h)

    # check if image size is too small
    if cols > W or rows > H:
        print("Image too small for specified cols!")
        exit(0)

    # ascii image is a list of character strings
    aimg = []
    # generate list of dimensions
    for j in range(rows):
        y1 = int(j * h)
        y2 = int((j + 1) * h)
        # correct last tile
        if j == rows - 1:
            y2 = H
        # append an empty string
        aimg.append("")
        for i in range(cols):
            # crop image to tile
            x1 = int(i * w)
            x2 = int((i + 1) * w)
            # correct last tile
            if i == cols - 1:
                x2 = W
            # crop image to extract tile
            img = image.crop((x1, y1, x2, y2))
            # get average luminance
            avg = int(getAverageL(img))
            # look up ascii char
            if moreLevels:
                gsval = gscale1[int((avg * 69) / 255)]
            else:
                gsval = gscale2[int((avg * 9) / 255)]
            # append ascii char to string
            aimg[j] += gsval

    # return txt image
    return aimg


def get_ascii_frames(gif_file, cols, scale, moreLevels):
    text_frames = []
    with Image.open(gif_file) as im:
        im.seek(1)  # skip to the second frame
        try:
            while 1:
                im.seek(im.tell() + 1)                
                aimg = covertImageToAscii(im, cols, scale, moreLevels)
                screen_text = ''
                for row in aimg:
                    postfix =  '' if screen_text == '' else "\\"+'n'
                    screen_text += postfix + row.replace("\\","\\"+"\\") # fix 1
                text_frames.append(screen_text)
                print(cols, gif_file, len(text_frames))
        except EOFError:
            pass  # end of sequence

    frames_len = str(len(text_frames))
    cs_frames=''
    for frame in text_frames:
        prefix = '' if cs_frames=='' else ','
        cs_frames+=prefix+'"'+frame.replace('"',"\\"+'"')+'"'

    return cs_frames, frames_len


def se_code(cs_frames, frames_len):
    return """int game_state=0;
        int frames_count="""+frames_len+""";
        string[] frames={"""+cs_frames+"""};

        public Program()
        {
            game_state = Convert.ToInt32(Storage);
            Runtime.UpdateFrequency = UpdateFrequency.Update1;
        }

        public void Save()
        {
            Storage = game_state.ToString();
        }

        public void Main(string argument, UpdateType updateSource)
        {
            var lcd = GridTerminalSystem.GetBlockWithName("lcd") as IMyTextPanel;
            lcd.WriteText(frames[game_state]);
            game_state++;
            if (game_state >= frames_count) game_state = 0;
        }
        """


def cs_code(cs_frames, frames_len, infinity_loop):    
    infinity_loop = 'while(true) ' if infinity_loop else ''
    return """using System;
using System.Threading;
namespace AsciiArt
{
    class draw
    {
        static void Main() 
        {
        string[] frames={"""+cs_frames+"""};        
        """+infinity_loop+""" for(int i=0;i<"""+frames_len+""";i++)
            {
                Console.Clear();
                Console.Write(frames[i]);
                Thread.Sleep(100);
            }
        }
    }
}
"""


def se_save(cs, script_len_limit, se_file_name):
    if len(cs)>script_len_limit:
        print('Caution!\nScript length: '+str(len(cs))+' exceeds SE program block script length limit')
        return False
    else:
        with open(se_file_name,'w') as file:
            file.write(cs)
        file.close()
        print('Script of '+str(len(cs))+' symbols length saved sucesfully')
        return True


def cs_save(cs, se_file_name):    
    with open(se_file_name,'w') as file:
        file.write(cs)
    file.close()


def main():
    if len(sys.argv)!=5:
        print("Usage: python3 gif-to-ascii.py cols, step, script_length_limit, morelevels")
        print("Example:")
        print("python3 gif-to-ascii.py 80 10 100000 0")
        sys.exit(1)

    # set scale default as 0.43 which suits a Courier font
    script_len_limit = int(sys.argv[3]) # 100000
    scale = 0.43
    moreLevels = int(sys.argv[4])
    step = int(sys.argv[2])
    

    # read gif files
    files = os.listdir('gifs/')
    for file_name in files:
        gif_file = 'gifs/'+file_name
        se_file_name = 'se/'+(file_name[:-4])+'.cs'
        cs_file_name = 'cs/'+(file_name[:-4])+'.cs'
        cols = int(sys.argv[1])
        while cols>0:

            cs_frames, frames_len = get_ascii_frames(gif_file, cols, scale, moreLevels)
            
            cs = se_code(cs_frames, frames_len)
            if se_save(cs, script_len_limit, se_file_name)==False:
                cols -= step
                continue

            cs = cs_code(cs_frames, frames_len, True)
            cs_save(cs, cs_file_name)
            break


if __name__ == '__main__':
    main()
