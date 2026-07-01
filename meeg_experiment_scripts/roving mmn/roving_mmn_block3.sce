# Mismatch negativity task (Roving paradigm) for the DFP project(Ece Kocagoncu,2017)
# ek390@cam.ac.uk

# Block 3

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
sound { wavefile { filename = "Freq400.wav"; preload = true; }; attenuation = 0.25;} f400;
sound { wavefile { filename = "Freq450.wav"; preload = true; }; attenuation = 0.25;} f450;
sound { wavefile { filename = "Freq500.wav"; preload = true; }; attenuation = 0.25;} f500;
sound { wavefile { filename = "Freq550.wav"; preload = true; }; attenuation = 0.25;} f550;
sound { wavefile { filename = "Freq600.wav"; preload = true; }; attenuation = 0.25;} f600;
sound { wavefile { filename = "Freq650.wav"; preload = true; }; attenuation = 0.25;} f650;
sound { wavefile { filename = "Freq700.wav"; preload = true; }; attenuation = 0.25;} f700;
sound { wavefile { filename = "Freq750.wav"; preload = true; }; attenuation = 0.25;} f750;
sound { wavefile { filename = "Freq800.wav"; preload = true; }; attenuation = 0.25;} f800;

video { filename = "penguin3-1.xvid.avi"; 	height = 450; width = 800; end_time = 154500;} penguin31;
video { filename = "penguin3-2.xvid.avi"; 	height = 450; width = 800; end_time = 156500;} penguin32; 


trial {
	trial_duration = 1000;
	
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
	video penguin31;
	time = 0;
	#port_code = 20;
	
	TEMPLATE "roving.tem" {
		soundfile condition trigger	;
		TEMPLATE "rov3-1.txt";
	};
};


trial {
	video penguin32;
	time = 0;
	#port_code = 20;
	
	TEMPLATE "roving.tem" {
		soundfile condition trigger	;
		TEMPLATE "rov3-2.txt";
	};
};

# more instructions
trial {
	trial_duration = forever;
	trial_type = specific_response;
	terminator_button = 2;
	
	picture {
		text {
			caption = "You have completed the task! :) \n\n Please have a short break now.";
			background_color = 200,200,200;
			font_color = 0,0,0;
			width = 700;
			height = 600;
		};
	x = 0; y = 0;
	};
};