# Mismatch negativity task (Roving paradigm) for the DFP project(Ece Kocagoncu,2017)
# ek390@cam.ac.uk

# Block 1

#parameters
scenario = "roving_MMN";
default_font_size = 24;
active_buttons = 2;
button_codes = 1,2;
default_background_color = 200,200,200;
default_font = "Arial";
default_text_color = 0,0,0;
write_codes = true; #send triggers
pulse_width = 50; 
response_matching = simple_matching;
no_logfile = false;

begin;

#objects
sound { wavefile { filename = "Freq400.wav"; preload = true; }; attenuation = 0;} f400;
sound { wavefile { filename = "Freq450.wav"; preload = true; }; attenuation = 0;} f450;
sound { wavefile { filename = "Freq500.wav"; preload = true; }; attenuation = 0;} f500;
sound { wavefile { filename = "Freq550.wav"; preload = true; }; attenuation = 0;} f550;
sound { wavefile { filename = "Freq600.wav"; preload = true; }; attenuation = 0;} f600;
sound { wavefile { filename = "Freq650.wav"; preload = true; }; attenuation = 0;} f650;
sound { wavefile { filename = "Freq700.wav"; preload = true; }; attenuation = 0;} f700;
sound { wavefile { filename = "Freq750.wav"; preload = true; }; attenuation = 0;} f750;
sound { wavefile { filename = "Freq800.wav"; preload = true; }; attenuation = 0;} f800;

video { filename = "penguin1-1.xvid.avi"; 	height = 450; width = 800; end_time = 154000;} penguin11; #likes xvid so much
video { filename = "penguin1-2.xvid.avi"; 	height = 450; width = 800; end_time = 158000;} penguin12;  

#instructions
trial {
	trial_duration = forever;
	trial_type = first_response;
	
	picture {
		text {
			caption = "
Today's tasks:\n
Sound check   2 min  COMPLETED
Watch documentary   10 min  ...
Letter detection task   15 min  ...
Perceptual task   8 min   ...
Moon detection task   10 min  ...
Resting eyes open  5 min   ...
Resting eyes closed  5 min  ...\n
Press button to continue.";
			background_color = 200,200,200;
			font_color = 0,0,0;
			width = 700;
			height = 600;
		};
	x = 0; y = 0;
	};
};

trial {
	trial_duration = forever;
	trial_type = first_response;
	
	picture {
		text {
			caption = "In the next 10 min, you will \n be watch a short clip from a \n nature documentary. \n\n As you watch you will hear \n sounds in the background. Please \n ignore them, just relax and \n enjoy the movie. \n\n Press button to proceed.";
			background_color = 200,200,200;
			font_color = 0,0,0;
			width = 700;
			height = 600;
		};
	x = 0; y = 0;
	};
};

#HPI
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
		};
	x = 0; y = 0;
	};
};

trial {
	trial_duration = 500;
	
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
};

trial {
	video penguin11;
	time = 0;
	#port_code = 20;
	
	TEMPLATE "roving.tem" {
		soundfile condition trigger	;
		TEMPLATE "rov1-1.txt";
	};
};

trial {
	video penguin12;
	time = 0;
	#port_code = 20;
	
	TEMPLATE "roving.tem" {
		soundfile condition trigger	;
		TEMPLATE "rov1-2.txt";
	};
};

trial {
	trial_duration = forever;
	trial_type = specific_response;
	terminator_button = 2;
	
	picture {
		text {
			caption = "You have completed 1 of 2 parts. \n Please have a short break now.";
			background_color = 200,200,200;
			font_color = 0,0,0;
			width = 700;
			height = 600;
		};
	x = 0; y = 0;
	};
};


