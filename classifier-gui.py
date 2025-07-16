import os
import pygame
import csv
import image_shredder
import re
import math
from natsort import natsorted

# Initialize Pygame
pygame.init()

# Colors
white = (255, 255, 255) 
black = (0, 0, 0)
green = (170, 180, 100)
forest = (105,130,100)
background = (45, 40, 40) 
button = (75, 70, 70) 
beige = (215, 190, 150) 
cyan = (125,175,160)
pink = (210,130,150)
orange = (230,140,80)
yellow = (215,165,90)
neon_purple = (255, 50, 255)
bright_red = (220, 50, 50)


# Set up the display
infoObject = pygame.display.Info()
HEIGHT = int(infoObject.current_h/(2**0.5))
WIDTH = int(infoObject.current_w/(2**0.5))
scrn = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Fecundity Tile Classifier')

# Handle Text
font = pygame.font.Font('freesansbold.ttf', 32)

start_text = font.render('Drag your file here to get started!', True, cyan)
start_textRect = start_text.get_rect()
start_textRect.center = (WIDTH // 2, HEIGHT // 2)

loading_text = font.render('Loading...', True, cyan)
loading_textRect = loading_text.get_rect()
loading_textRect.center = (WIDTH // 2, HEIGHT // 2)

genTiles_text = font.render('Generating Tiles...', True, cyan)
genTiles_textRect = genTiles_text.get_rect()
genTiles_textRect.center = (WIDTH // 2, HEIGHT // 2)

genCSV_text = font.render('Generating CSV...', True, cyan)
genCSV_textRect = genCSV_text.get_rect()
genCSV_textRect.center = (WIDTH // 2, HEIGHT // 2)

genCSVprogress_text = font.render('0 / 0', True, cyan)
genCSVprogress_textRect = genCSVprogress_text.get_rect()
genCSVprogress_textRect.center = (WIDTH // 2, int((5/8) * HEIGHT))

checkWhitespace_text = font.render('Checking Whitespaces...', True, cyan)
checkWhitespace_textRect = checkWhitespace_text.get_rect()
checkWhitespace_textRect.center = (WIDTH // 2, HEIGHT // 2)

clearWhitespace_text = font.render('Clearing Whitespaces...', True, cyan)
clearWhitespace_textRect = clearWhitespace_text.get_rect()
clearWhitespace_textRect.center = (WIDTH // 2, HEIGHT // 2)

whitespaceprogress_text = font.render('0 / 0', True, cyan)
whitespaceprogress_textRect = whitespaceprogress_text.get_rect()
whitespaceprogress_textRect.center = (WIDTH // 2, int((5/8) * HEIGHT))

buttonfont = pygame.font.Font('freesansbold.ttf', 16)

progressfont = pygame.font.Font('freesansbold.ttf', 12)

button1_text = buttonfont.render('1 Egg', True, beige)
button1_textRect = button1_text.get_rect()
button1_Rect = button1_textRect.scale_by(3)
button1_Rect.center = (int(2.5/8 * WIDTH), int((6/7)*HEIGHT)) 
button1_textRect.center = button1_Rect.center

button2_text = buttonfont.render('Unsure', True, beige)
button2_textRect = button2_text.get_rect()
button2_Rect = button1_textRect.scale_by(3)
button2_Rect.center = (int(5.5/8 * WIDTH), int((6/7)*HEIGHT))
button2_textRect.center = button2_Rect.center


button0_text = buttonfont.render('0 Eggs', True, beige)
button0_textRect = button0_text.get_rect()
button0_Rect = button1_textRect.scale_by(3)
button0_Rect.center = (int(1/8 * WIDTH), int((6/7)*HEIGHT))
button0_textRect.center = button0_Rect.center

custom_count = 10
buttonC_text = buttonfont.render(f'Custom: {custom_count}', True, beige)
buttonC_textRect = buttonC_text.get_rect()
buttonC_Rect = button1_textRect.scale_by(3)
buttonC_Rect.center = (int(4/8 * WIDTH), int((6/7)*HEIGHT))
buttonC_textRect.center = buttonC_Rect.center


buttonU_text = buttonfont.render('Undo', True, beige)
buttonU_textRect = buttonU_text.get_rect()
buttonU_Rect = button1_textRect.scale_by(3)
buttonU_Rect.center = (int(7/8 * WIDTH), int((6/7)*HEIGHT))
buttonU_textRect.center = buttonU_Rect.center



def get_pt(tile_name): 
  ''' Takes in a tile path name and returns the value of the slice '''
  return int(tile_name[tile_name.index("pt")+2:tile_name.index(".", tile_name.index("pt"))])


# Main loop for file input gui
gettingFile = True
while gettingFile:
    # --- Display Handling ---
    scrn.fill(background)
    scrn.blit(start_text, start_textRect)
    # Select theme buttons in the bottom: white, red, green, blue, maybe paste yellow orange and purple too

    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gettingFile = False
            pygame.quit()
        elif event.type == pygame.DROPFILE:
            file_path = event.file
            print(f"File dropped: {file_path}")
            # Get the directory of the dropped file
            directory = os.path.dirname(file_path)
            file = file_path[len(directory)+1:]
            gettingFile = False
            scrn.fill(background)
            scrn.blit(loading_text, loading_textRect)
    pygame.display.flip()


# Handle files
slice_path = file_path
if file.endswith("sliced"):
  csv_path = directory + "/" + file[:file.index("sliced")-1] + ".csv"
  file_path = slice_path[:slice_path.index("sliced")-1]
else:
  csv_path = f"{directory}/{file}.csv"
  if not (os.path.isdir(f"{file_path}-sliced")):
    # Make sure this file doesn't already have the sliced images:
    first_image_path = os.path.join(file_path, os.listdir(file_path)[0])
    first_image = pygame.image.load(first_image_path)
    height = first_image.get_height()
    width = first_image.get_width()
    if (height != 75 or width != 75):
      # Generate slices
      scrn.fill(background)
      scrn.blit(genTiles_text, genTiles_textRect)
      pygame.display.flip()
      image_shredder.main(file_path)
      slice_path += "-sliced"
  else:
    slice_path += "-sliced"

# Initiate csv
if not os.path.isfile(csv_path):
  print("Intitating CSV...")
  with open(csv_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(["Image", "Part", "Count", "Whitespace"])
    tile_names = [t for t in os.listdir(slice_path)]
    # Generate a list to order using the name of each tile, without old egg count
    tile_numbering = []
    for t in range(len(tile_names)):
      current_tile = tile_names[t]
      if tile_names[t].startswith("eggs"):
        tile_numbering.append((current_tile[current_tile.index('count')+5:], current_tile))
      else:
        tile_numbering.append((current_tile, current_tile))
    # sort by name, then save the actual name of the tile (not used for sorting)
    tile_names = [row[1] for row in natsorted(tile_numbering)]
    display_len = len(tile_names)
    display_t = 0
    t = 0
    while t < len(tile_names):
      if (not (tile_names[t][-4:] == '.jpg' or tile_names[t][-4:] == '.png')) or tile_names[t].startswith('.'):
        del tile_names[t] #Exclude non images
        display_t += 1
      else:
        tile_name = tile_names[t][:tile_names[t].index("pt")-1]
        if tile_names[t].startswith("eggs"):
          try:
            val = tile_names[t][4:tile_names[t].index("count")]
            if val == "unsure":
              val.capitalize()
            #Rename original file to exclude the eggsNcount part of the name
            old_path = tile_names[t]
            new_path = old_path[old_path.index('count')+5:]
            #If val is not none, exclude eggsNcount from tile name
            tile_name = tile_name[tile_name.index('count')+5:] 
            if os.path.isfile(os.path.join(slice_path, old_path)): 
              os.rename(os.path.join(slice_path, old_path), os.path.join(slice_path, new_path))
          except: # if "count" doesn't appear
            val = None
        else:
          val = None        
        writer.writerow([tile_name] + [get_pt(tile_names[t])] + [val] + [None])
        t += 1
        display_t += 1
      genCSVprogress_text = font.render(f'{display_t} / {display_len}', True, cyan)
      genCSVprogress_textRect = genCSVprogress_text.get_rect()
      genCSVprogress_textRect.center = (WIDTH // 2, int((5/8) * HEIGHT))
      scrn.fill(background)
      scrn.blit(genCSV_text, genCSV_textRect)
      scrn.blit(genCSVprogress_text, genCSVprogress_textRect)
      pygame.display.flip()

print(f"CSV Path: {csv_path}")

# Clear whitespaces
def tile_from_csv(name, part):
  return f"{name} pt{part}.jpg"
IMAGE = 0
PART = 1
COUNT = 2
WHITESPACE = 3
print("Checking Whitespaces...")
scrn.fill(background)
scrn.blit(checkWhitespace_text, checkWhitespace_textRect)
pygame.display.flip()
with open(csv_path, mode='r') as original:
    check_reader = csv.reader(original, delimiter=',', quotechar='|')
    headings = next(check_reader)
    first_row = next(check_reader)
if first_row[WHITESPACE] == "True" or first_row[WHITESPACE] == "False":
  print("Already Cleared.")
else:
  csv_temp = csv_path[:-4]+'.tmp'
  with open(csv_path, mode='r') as oldfile, open(csv_temp, mode='w', newline='') as newfile:
    print("Clearing Whitespaces...")
    reader = csv.reader(oldfile, delimiter=',', quotechar='|')
    writer = csv.writer(newfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    start = True
    oldfile.seek(0)
    row_count = sum(1 for row in reader)
    oldfile.seek(0)
    reader_index = 1
    for row in reader:
      print(row)
      scrn.fill(background)
      whitespaceprogress_text = font.render(f'{reader_index} / {row_count}', True, cyan)
      whitespaceprogress_textRect = whitespaceprogress_text.get_rect()
      whitespaceprogress_textRect.center = (WIDTH // 2, int((5/8) * HEIGHT))
      scrn.blit(clearWhitespace_text, clearWhitespace_textRect)
      scrn.blit(whitespaceprogress_text, whitespaceprogress_textRect)
      pygame.display.flip()
      if start:
        writer.writerow(["Image", "Part", "Count", "Whitespace"])
        start = False
      else:
        reader_index += 1
        tile = tile_from_csv(row[IMAGE], row[PART])
        tilepath = os.path.join(slice_path, tile)
        has_whitespace = False
        if os.path.isfile(tilepath):
          file_size_kb = os.stat(tilepath).st_size / 1024
          if file_size_kb <= 1.46:
            has_whitespace = True
            count = 0
          else:
            has_whitespace = False
        if not has_whitespace:
          count = row[COUNT]
        writer.writerow([row[IMAGE]] + [row[PART]] + [count] + [has_whitespace]) # why would I add something that isn't a tile?
  os.replace(csv_temp, csv_path)


def classify_tile(value, csv_path):
  csv_temp = csv_path[:-4]+'.tmp'
  with open(csv_path, mode='r') as oldfile, open(csv_temp, mode='w', newline='') as newfile:
    reader = csv.reader(oldfile, delimiter=',', quotechar='|')
    writer = csv.writer(newfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    oldfile.seek(0)
    found = False
    for row in reader:
      if (not found) and (row[COUNT] == ''):
        writer.writerow([row[IMAGE]] + [row[PART]] + [value] + [row[WHITESPACE]])
        found = True
      else:
        writer.writerow([row[IMAGE]] + [row[PART]] + [row[COUNT]] + [row[WHITESPACE]])
  os.replace(csv_temp, csv_path)

def undo_tile(csv_path):
  # First, find the index to undo, skipping whitespaces
  with open(csv_path, mode='r') as file:
    search_reader = csv.reader(file, delimiter=',', quotechar='|')
    file.seek(0)
    index = 0
    consecutive_whitespaces = 0
    for row in search_reader:
      if row[COUNT] == '':
        break
      if row[WHITESPACE] == 'True':
        consecutive_whitespaces += 1
      else:
        consecutive_whitespaces = 0
      index += 1

  undo_index = index-consecutive_whitespaces-1
  if undo_index < 1: # 0 is header
    return  # If there is nothing to undo, exit the function.

  csv_temp = csv_path[:-4]+'.tmp'
  with open(csv_path, mode='r') as oldfile, open(csv_temp, mode='w', newline='') as newfile:
    reader = csv.reader(oldfile, delimiter=',', quotechar='|')
    writer = csv.writer(newfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    oldfile.seek(0)
    index = 0
    for row in reader: 
      if index == undo_index:
        row[COUNT] = None
      writer.writerow([row[IMAGE]] + [row[PART]] + [row[COUNT]] + [row[WHITESPACE]])
      index += 1
  os.replace(csv_temp, csv_path)

def next_image(csv_path): 
  with open(csv_path, mode='r') as file:
    reader = csv.reader(file, delimiter=',', quotechar='|')
    file.seek(0)
    found = False
    for row in reader:
      if row[COUNT] == '':
        img = row[IMAGE]
        pt = row[PART]
        return tile_from_csv(img, pt), f"{img}.png"
    img = row[IMAGE] # If no next image, just keep to the last one
    pt = row[PART]
    return tile_from_csv(img, pt), f"{img}.png"

def how_many_counted(csv_path):
  counted = 0
  total = 0
  with open(csv_path, mode='r') as file:
    reader = csv.reader(file, delimiter=',', quotechar='|')
    file.seek(0)
    for row in reader:
      if not (row[COUNT] == ''):
        counted += 1
      total += 1
  return counted, total



# Main loop for tile classification gui
clock = pygame.time.Clock()
running = True
NORMAL = 0
CUSTOM = 1
mode = NORMAL
classify_value = 0
show_all_tiles = False
print("Starting...")
current_tile, current_cap = next_image(csv_path)
imgscale = int(5/8 * HEIGHT)
tile_img = pygame.image.load(slice_path+"/"+f"{current_tile}")
tile_img = pygame.transform.scale(tile_img, (imgscale, imgscale))
width_offset = int((WIDTH-2*(imgscale))/3)
height_offset = int(3/32 * HEIGHT)
nocap = False
try:
  cap_img = pygame.image.load(file_path+"/"+f"{current_cap}")
  scale_ratio = imgscale/cap_img.get_width()
  tile_indent = int(((cap_img.get_width()%75)/2)*scale_ratio)
  cap_img = pygame.transform.scale(cap_img, (imgscale, imgscale))
  tile_rect_H = math.ceil((cap_img.get_width()-(2*tile_indent))/10)
  tile_Rect = pygame.Rect((width_offset+tile_indent+(math.floor((get_pt(current_tile)-1)/10))*tile_rect_H, 
        height_offset+tile_indent+(((get_pt(current_tile)-1)%10)*tile_rect_H)), (tile_rect_H, tile_rect_H))
  tile_img_Rect = pygame.Rect(WIDTH-imgscale-width_offset, height_offset, imgscale, imgscale)
except: 
  nocap = True
  tile_img_Rect = pygame.Rect(int((WIDTH-imgscale)/2), height_offset, imgscale, imgscale)

progress, total = how_many_counted(csv_path)
progress_bar_text = progressfont.render(f'{progress-1} / {total-1}', True, beige)
progress_bar_textRect = buttonU_text.get_rect()
progress_bar_Rect = pygame.Rect((width_offset, int(59.5/64 * HEIGHT)), (WIDTH-2*width_offset, int(1/32 * HEIGHT)))
progress_bar_textRect.center = buttonC_Rect.center
progress_bar_textRect.center = progress_bar_Rect.center
progress_bar_textRect.top = progress_bar_textRect.top + int(HEIGHT/256)
progress_done_Rect = progress_bar_Rect.copy()
progress_done_Rect.width = int(progress_bar_Rect.width * progress/total)
dots = []
while running:
    # --- Display Handling ---
    scrn.fill(background)

    mousepos = pygame.mouse.get_pos()

    button_curve = int(HEIGHT/100)
    button_outline = int(HEIGHT/500)

    # Buttons
    buttoncollision = None
    if button0_Rect.collidepoint(mousepos):
      pygame.draw.rect(scrn, button, button0_Rect, border_radius=button_curve)
      buttoncollision = 0
    else:
      pygame.draw.rect(scrn, button, button0_Rect, button_outline, border_radius=button_curve)
    scrn.blit(button0_text, button0_textRect)

    if button1_Rect.collidepoint(mousepos):
      pygame.draw.rect(scrn, button, button1_Rect, border_radius=button_curve)
      buttoncollision = 1
    else:
      pygame.draw.rect(scrn, button, button1_Rect, button_outline, border_radius=button_curve)
    scrn.blit(button1_text, button1_textRect)

    if button2_Rect.collidepoint(mousepos):
      pygame.draw.rect(scrn, button, button2_Rect, border_radius=button_curve)
      buttoncollision = 2
    else:
      pygame.draw.rect(scrn, button, button2_Rect, button_outline, border_radius=button_curve)
    scrn.blit(button2_text, button2_textRect)

    if buttonC_Rect.collidepoint(mousepos):
      pygame.draw.rect(scrn, button, buttonC_Rect, border_radius=button_curve)
      buttoncollision = 3
    else:
      pygame.draw.rect(scrn, button, buttonC_Rect, button_outline, border_radius=button_curve)
    scrn.blit(buttonC_text, buttonC_textRect)

    if buttonU_Rect.collidepoint(mousepos):
      pygame.draw.rect(scrn, button, buttonU_Rect, border_radius=button_curve)
      buttoncollision = 4
    else:
      pygame.draw.rect(scrn, button, buttonU_Rect, button_outline, border_radius=button_curve)
    scrn.blit(buttonU_text, buttonU_textRect)

    pygame.draw.rect(scrn, button, progress_bar_Rect)#, border_radius=button_curve)
    pygame.draw.rect(scrn, forest, progress_done_Rect)#, border_radius=button_curve)
    scrn.blit(progress_bar_text, progress_bar_textRect)


    # Image
    if nocap:
      scrn.blit(tile_img, (int((WIDTH-imgscale)/2), height_offset))
    else:
      scrn.blit(cap_img, (width_offset, height_offset))
      scrn.blit(tile_img, (WIDTH-imgscale-width_offset, height_offset))
      if show_all_tiles:
        for i in range(1, 101):
          tilegrid_Rect = pygame.Rect((width_offset+tile_indent+(math.floor((i-1)/10))*tile_rect_H, 
              height_offset+tile_indent+(((i-1)%10)*tile_rect_H)), (tile_rect_H, tile_rect_H))
          pygame.draw.rect(scrn, black, tilegrid_Rect, button_outline)
      pygame.draw.rect(scrn, yellow, tile_Rect, button_outline)

    for dot in dots:
      pygame.draw.circle(scrn, bright_red, dot[0], dot[1])


    # --- Event Handling ---
    classify_event = False
    undo_event = False
    update_custom = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if mode != CUSTOM:
              if event.key == pygame.K_0:
                classify_event = True
                classify_value = 0
              if event.key == pygame.K_1:
                classify_event = True
                classify_value = 1
              if event.key == pygame.K_2:
                classify_event = True
                classify_value = 2
              if event.key == pygame.K_3:
                classify_event = True
                classify_value = 3
              if event.key == pygame.K_4:
                classify_event = True
                classify_value = 4
              if event.key == pygame.K_5:
                classify_event = True
                classify_value = 5
              if event.key == pygame.K_6:
                classify_event = True
                classify_value = 6
              if event.key == pygame.K_7:
                classify_event = True
                classify_value = 7
              if event.key == pygame.K_8:
                classify_event = True
                classify_value = 8
              if event.key == pygame.K_9:
                classify_event = True
                classify_value = 9
              if event.key == pygame.K_s:
                classify_event = True
                classify_value = custom_count
              if event.key == pygame.K_t:
                show_all_tiles = not show_all_tiles
              if event.key == pygame.K_c or event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                classify_event = True
                classify_value = custom_count
              if event.key == pygame.K_u:
                classify_event = True
                classify_value = "Unsure"
              if event.key == pygame.K_z:
                undo_event = True
              if event.key == pygame.K_f: # Toggle Fullscreen #TODO: for version 1.1.1
                if infoObject.current_h == HEIGHT:
                  HEIGHT = int(infoObject.current_h/(2**0.5))
                  WIDTH = int(infoObject.current_w/(2**0.5))
                else:
                  HEIGHT = infoObject.current_h
                  WIDTH = infoObject.current_w
                #TODO: also need to redefine every rect for buttons, images, and the progress bar with the new dimensions.
                scrn = pygame.display.set_mode((WIDTH, HEIGHT))
              if event.key == pygame.K_UP:
                custom_count += 1
                buttonC_text = buttonfont.render(f'Custom: {custom_count}', True, beige)
                buttonC_textRect = buttonC_text.get_rect()
                buttonC_textRect.center = buttonC_Rect.center
                up_timer = 10
              if event.key == pygame.K_DOWN:
                if custom_count > 0:
                  custom_count -= 1
                  buttonC_text = buttonfont.render(f'Custom: {custom_count}', True, beige)
                  buttonC_textRect = buttonC_text.get_rect()
                  buttonC_textRect.center = buttonC_Rect.center
                  down_timer = 10
        elif event.type == pygame.MOUSEBUTTONUP:
          if buttoncollision == 0:
            classify_event = True
            classify_value = 0
          if buttoncollision == 1:
            classify_event = True
            classify_value = 1
          if buttoncollision == 2:
            classify_event = True
            classify_value = "Unsure"
          if buttoncollision == 3:
            classify_event = True
            classify_value = custom_count
          if buttoncollision == 4:
            undo_event = True
          remove_index = -1
          for d in range(len(dots)):
            if math.sqrt((mousepos[0]-dots[d][0][0])**2 + (mousepos[1]-dots[d][0][1])**2) <= dots[d][1]:
              remove_index = d
          if remove_index > -1:
            del dots[remove_index]
            custom_count = len(dots)
            update_custom = True
          if tile_img_Rect.collidepoint(mousepos) and not (remove_index > -1):
            dots.append((mousepos, int(HEIGHT/128)))
            custom_count = len(dots)
            update_custom = True


    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
      if up_timer > 0:
        up_timer -= 1
      else:
        custom_count += 1
        update_custom = True
    elif keys[pygame.K_DOWN]:
      if down_timer > 0:
        down_timer -= 1
      else:
        if custom_count > 0:
          custom_count -= 1
          update_custom = True
    if classify_event: 
      classify_tile(classify_value, csv_path)
      if progress < total:
        progress += 1
    if undo_event: 
      undo_tile(csv_path)
      if progress > 1:
        progress -= 1
    if classify_event or undo_event:
      current_tile, current_cap = next_image(csv_path)
      tile_img = pygame.image.load(slice_path+"/"+f"{current_tile}")
      tile_img = pygame.transform.scale(tile_img, (imgscale, imgscale))
      if not nocap:
        try: # check if path exists before displaying. If it doesn't, still display tile.
          cap_img = pygame.image.load(file_path+"/"+f"{current_cap}")
          cap_img = pygame.transform.scale(cap_img, (imgscale, imgscale))
        except:
          cap_img = pygame.Surface((imgscale, imgscale))
        tile_Rect = pygame.Rect((width_offset+tile_indent+(math.floor((get_pt(current_tile)-1)/10))*tile_rect_H, 
              height_offset+tile_indent+(((get_pt(current_tile)-1)%10)*tile_rect_H)), (tile_rect_H, tile_rect_H))
      progress_bar_text = progressfont.render(f'{progress-1} / {total-1}', True, beige)
      progress_bar_textRect = buttonU_text.get_rect()
      progress_bar_textRect.center = progress_bar_Rect.center
      progress_bar_textRect.top = progress_bar_textRect.top + int(HEIGHT/256)
      progress_done_Rect = progress_bar_Rect.copy()
      progress_done_Rect.width = int(progress_bar_Rect.width * progress/total)
      dots = []
    if update_custom:
      buttonC_text = buttonfont.render(f'Custom: {custom_count}', True, beige)
      buttonC_textRect = buttonC_text.get_rect()
      buttonC_textRect.center = buttonC_Rect.center




            
    pygame.display.flip()
    clock.tick(15)

pygame.quit()


#Build: python3 -m PyInstaller -w classifier-gui.py --icon=egg_icon.png