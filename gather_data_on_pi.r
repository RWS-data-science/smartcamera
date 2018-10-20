library(rPython)
library(jpeg)

dir = '/media/pi/A894-0C66/day3_1024'

system('teamviewer')
system('sudo gpsd -n /dev/ttyS0 -F /var/run/gpsd.sock')



python.load('lees_gps.py')

i=0

location_old = c()


while(0<1){
  
  print(i)
  i = i+1
  
  #get time
  time = Sys.time()
  time = gsub(time , replacement =  '_', pattern = ' ')
  ##
  
  #take photo
  file_name_image = paste0(i,'.jpg')
  command = paste0('raspistill -o ', file.path(dir ,file_name_image), ' -w 1024 -h 1024 --nopreview -t 2000')
  system(command)
  ##
  
  #get location
  location = unlist(python.call('get_location'))
  file_name_gps = paste0(i,'.txt')
  write( append(location, time), file.path(dir ,file_name_gps))
  print(location)
 
  
  
}


