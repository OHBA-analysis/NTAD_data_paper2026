#Scene repetition task for the DFP project(Ece Kocagoncu,2017)
#ek390@cam.ac.uk


#parameters
scenario = "Scenes";
default_font_size = 24;
active_buttons = 2;
button_codes = 60,61;
default_background_color = 200,200,200;
default_font = "Arial";
default_text_color = 0,0,0;

write_codes = true; #send triggers
pulse_width = 50;
response_matching = simple_matching;
no_logfile = false;

begin;

#practice trial list
array {
	bitmap { filename = "pscene1.jpg"; preload = false; width = 650; height = 488; };
	bitmap { filename = "pscene2.jpg"; preload = false; width = 650; height = 488; };
	bitmap { filename = "pscene3.jpg"; preload = false; width = 650; height = 488; };
	bitmap { filename = "pspace1.jpg"; preload = false; width = 650; height = 488; };
	bitmap { filename = "pscene4.jpg"; preload = false; width = 650; height = 488; };
	bitmap { filename = "pscene5.jpg"; preload = false; width = 650; height = 488; };
	bitmap { filename = "pscene6.jpg"; preload = false; width = 650; height = 488; };
	bitmap { filename = "pscene7.jpg"; preload = false; width = 650; height = 488; };
	bitmap { filename = "pspace2.jpg"; preload = false; width = 650; height = 488; };
	bitmap { filename = "pscene8.jpg"; preload = false; width = 650; height = 488; };
	bitmap { filename = "pscene9.jpg"; preload = false; width = 650; height = 488; };
	bitmap { filename = "pscene10.jpg"; preload = false; width = 650; height = 488; };	
} practice_pics;

array {
	bitmap { filename = 	"scene1.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene2.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene3.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene4.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene5.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene6.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene7.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene8.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene9.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"space1.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene10.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene11.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene12.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene13.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene14.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene15.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene16.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene17.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene18.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene19.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"space2.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene20.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene21.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene22.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene23.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene24.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene25.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene26.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene27.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene5.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene7.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene4.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene8.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene28.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene3.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene9.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene10.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene29.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene30.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene31.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene32.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene13.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene33.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene1.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene11.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene34.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene35.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene15.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene6.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene36.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene12.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene14.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene37.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene18.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene21.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene2.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene16.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene38.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene20.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene39.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene40.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene41.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene42.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene17.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene23.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene25.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene43.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene44.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene28.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene26.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene45.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene46.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene47.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene48.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene30.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene49.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene50.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"space3.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene31.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene51.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene52.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene53.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene29.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"space4.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene54.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene32.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene55.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"space5.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene19.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene24.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene34.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene56.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene35.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene57.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene38.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene22.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene40.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene33.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene58.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene59.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene39.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene60.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene61.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene43.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene62.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene27.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene41.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene44.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene63.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene64.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene46.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene37.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene48.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene65.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene66.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene67.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene68.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene69.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene70.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"space6.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene36.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene50.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene47.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"space7.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene71.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene53.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene42.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene52.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene72.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene56.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene73.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene74.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene57.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene54.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene51.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene58.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene75.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene61.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene76.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene45.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene77.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene78.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene62.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene79.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene60.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene80.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene81.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene82.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene83.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene84.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene85.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene64.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene86.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene65.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene87.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene55.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene88.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene49.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene89.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene68.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene63.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene70.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene66.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene59.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene90.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene67.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene91.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene71.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene73.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene92.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene69.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene93.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene94.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"space8.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene95.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene96.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene97.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene72.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene76.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene98.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene80.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene79.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene81.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene99.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"space9.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene74.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"space10.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene84.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene100.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene85.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene77.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene101.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene83.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene102.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene75.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"space11.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene88.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene103.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene104.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene105.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene106.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene107.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene87.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"space12.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene108.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene90.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene86.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene78.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene109.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene89.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene95.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene92.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene94.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene96.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene110.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene111.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"space13.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene112.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene98.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene97.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene99.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene91.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene113.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene114.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene103.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene102.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene115.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene101.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene116.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene117.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene105.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene82.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene118.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene107.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene119.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene100.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene104.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene106.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene120.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene121.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene122.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene111.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene113.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene123.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene110.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene124.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene125.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene126.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene93.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene127.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene116.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene114.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene112.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene108.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene109.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene121.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene115.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene128.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene119.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene129.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene130.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene124.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene131.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene122.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene126.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene132.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene133.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene134.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene118.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene135.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene120.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene136.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene137.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene127.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene130.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene138.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene139.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene140.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene117.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene125.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene141.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene142.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene143.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene144.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene145.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene146.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene147.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene123.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene129.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene148.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene149.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene128.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene134.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene150.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"space14.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene151.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene133.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene152.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene137.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene153.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene138.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene139.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene154.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene155.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene132.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene156.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene157.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene142.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene131.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene140.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene141.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene135.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene136.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene158.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene147.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene145.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene159.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene146.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene160.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene161.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene144.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene162.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene163.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene149.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene164.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene165.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene143.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene153.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene166.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene150.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene156.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene155.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene152.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene158.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene159.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene167.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene168.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene161.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene169.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene160.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene162.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene170.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene164.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene171.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene165.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene172.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene173.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene174.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"space15.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene175.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene166.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene176.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene157.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene177.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene178.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene179.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene167.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene180.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene181.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene169.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene163.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene168.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene182.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene172.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene151.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene183.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene184.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene171.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene185.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene175.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene173.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene154.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene170.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene186.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene148.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene176.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene187.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene188.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene189.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"space16.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene190.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene179.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene181.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene191.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene183.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene192.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene178.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene193.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene185.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene194.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene195.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene174.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene184.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene186.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene196.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene197.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"space17.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene177.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene198.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene199.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene200.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene201.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene187.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene180.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene202.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene203.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene204.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene191.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene205.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene206.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene207.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene208.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene188.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene209.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene210.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene211.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene212.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene213.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene214.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene215.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene216.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene182.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene217.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene218.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene219.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene193.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene220.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene221.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene222.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"space18.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene192.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene190.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"space19.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene223.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene224.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"space20.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene195.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene225.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene226.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene227.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene199.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene196.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene198.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene228.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene201.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene229.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene202.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene230.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene197.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene189.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene231.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene206.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"space21.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene200.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene232.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene233.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene234.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene207.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene205.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene209.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene235.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene236.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene237.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene208.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene238.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene239.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene204.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene240.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene203.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene241.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene210.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene242.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene243.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene244.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene212.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene214.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene245.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene217.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene211.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene246.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene247.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene215.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene194.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene221.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene216.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"space22.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene223.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene248.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene249.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene222.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene220.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene218.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene224.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene250.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene251.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene252.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene213.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene253.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene229.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene228.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene254.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene231.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene219.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene227.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene255.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene256.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"space23.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene232.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene257.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene225.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene258.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene259.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"space24.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene230.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene260.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene261.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene262.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene263.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene264.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene226.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene265.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene266.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene235.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene238.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene267.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene268.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene239.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"space25.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene237.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene236.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene269.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene233.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene270.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene271.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene272.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene244.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene242.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene243.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene241.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"space26.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene240.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene273.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene234.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene245.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene251.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene249.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene274.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene275.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene276.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene277.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene278.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene253.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene252.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene248.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene247.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene250.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene254.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene259.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene258.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene257.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene279.jpg"	; preload = false; width = 650; height = 488; };
	bitmap { filename = 	"scene280.jpg"	; preload = false; width = 650; height = 488; };
} task_pics;


# types of trials

trial {
	trial_duration = forever;
	trial_type = first_response;
	
	picture {
		text {
			caption = "
Today's tasks:\n
Sound check   2 min  COMPLETED
Watch documentary   10 min  COMPLETED
Letter detection task   15 min  COMPLETED
Perceptual task   8 min  COMPLETED
Moon detection task   10 min  ...
Resting eyes open  5 min  ...
Resting eyes closed  5 min  ...\n
Press button to continue.";
			background_color = 200,200,200;
			font_color = 0,0,0;
			width = 700;
			height = 600;
		};
	x = 0; y = 0;
	};
} task_list;


# trial where participant can proceed to the next screen
trial {
	trial_duration = forever;
	trial_type = first_response;
	
	picture {
		text {
			caption = "In the next 10 min, you will be \n viewing a series of scenes presented quickly. \n\n Please focus your eyes on the + \n at the centre, and press the button \n with your right index finger when \n you see a scene with a moon in it. \n These moons will be large and \n obvious, so you would not miss it. \n\n Press button to proceed.";
			background_color = 200,200,200;
			font_color = 0,0,0;
			width = 700;
			height = 600;
		} textobj;
	x = 0; y = 0;
	};
} instruct_trial;

# trial that waits for experimenter's button press
trial {
	trial_duration = forever;
	trial_type = specific_response;
	terminator_button = 2;
	
	picture {
		text {
			caption = "We started recording. \n\n Please stay as still as \n possible from now on. \n\n We will begin shortly.";
			background_color = 200,200,200;
			font_color = 0,0,0;
			width = 700;
			height = 600;
		} ctrltextobj;
	x = 0; y = 0;
	};
} ctrl_instruct_trial;

# trial that shows picture
trial {
	trial_duration = 2000; #default value which will be changed in the loop
   trial_type = fixed;
   all_responses = false;

	picture {
		text {
			caption = "+";
			background_color = 200,200,200;
			font_color = 0,0,0;
			width = 700;
			height = 600;
		};
	x = 0; y = 0;
	};
	time = 0;
	duration = 300;
	
	stimulus_event {
		picture {
			background_color = 200,200,200;
			box { width = 650; height = 488; color = 100,100,100; }; #placeholder
			x = 0; y = 0;
		} scenepic;
		time = 300;
		code = "picture"; #condition default
		duration = 800;
		port_code = 33; # trigger default
	} picevent;

	stimulus_event{
		picture {
			text {
				caption = "+";
				background_color = 200,200,200;
				font_color = 0,0,0;
				width = 700;
				height = 600;
			};
		x = 0; y = 0;
		};
		time = 1100;
		duration = 5000; #jitter default
	} jitterevent;
	
} scene_trial;

######################################################################

begin_pcl;

# Open input file with durations and read into an array
int npics = practice_pics.count();

input_file durfile = new input_file;
array<int> durs[npics];
durfile.open("practice_durations.txt");

loop
	int i = 0
until
	i >= npics
begin
	i = i + 1;
	durs[i] = durfile.get_int();
end;
durfile.close();

input_file jitfile = new input_file;
array<int> jitters[npics];
jitfile.open("practice_jitters.txt");

loop
	int i = 0
until
	i >= npics
begin
	i = i + 1;
	jitters[i] = jitfile.get_int();
end;
jitfile.close();

###########################################################

task_list.present();
instruct_trial.present();
textobj.set_caption("We will start with a short \n practice, so that you can \n get used to the task. \n\n Press button to proceed.");
textobj.redraw();
instruct_trial.present();
ctrl_instruct_trial.present();

#present practice trials
loop
	int i = 1
until
	i >= npics
begin
	practice_pics[i].load();
	scenepic.set_part(1, practice_pics[i]);
	scene_trial.set_duration(durs[i]);
	picevent.set_event_code("practice");
	picevent.set_port_code(44);
	jitterevent.set_duration(jitters[i]);
	scene_trial.present();
	practice_pics[i].unload();
	i = i + 1;
end;

ctrltextobj.set_caption("Is everything clear?");
ctrltextobj.redraw();
ctrl_instruct_trial.present();

#present task trials

int npics2 = task_pics.count();
term.print("n pics: " + string(npics2) + "\n");

input_file durfile2 = new input_file;
array<int> durs2[npics2];
durfile2.open("task_durations.txt");

loop
	int i = 0
until
	i >= npics2
begin
	i = i + 1;
	durs2[i] = durfile2.get_int();
end;
durfile2.close();

input_file jitfile2 = new input_file;
array<int> jitters2[npics2];
jitfile2.open("task_jitters.txt");

loop
	int i = 0
until
	i >= npics2
begin
	i = i + 1;
	jitters2[i] = jitfile2.get_int();
end;
jitfile2.close();

input_file condfile = new input_file;
array<string> conds[npics2];
condfile.open("task_conditions.txt");

loop
	int i = 0
until
	i >= npics2
begin
	i = i + 1;
	conds[i] = condfile.get_string();
end;
condfile.close();

input_file trigfile = new input_file;
array<int> triggers[npics2];
trigfile.open("task_triggers.txt");

loop
	int i = 0
until
	i >= npics2
begin
	i = i + 1;
	triggers[i] = trigfile.get_int();
end;
trigfile.close();

loop
	int i = 1
until
	i >= npics2
begin
	task_pics[i].load();
	scenepic.set_part(1, task_pics[i]);
	scene_trial.set_duration(durs2[i]);
	picevent.set_event_code(conds[i]);
	picevent.set_port_code(triggers[i]);
	jitterevent.set_duration(jitters2[i]);
	scene_trial.present();
	task_pics[i].unload();
	i = i + 1;
end;

ctrltextobj.set_caption("You have completed the task! :) \n\n Please have a short break now.");
ctrltextobj.redraw();
ctrl_instruct_trial.present();




