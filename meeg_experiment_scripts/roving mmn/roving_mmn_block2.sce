# Mismatch negativity task (Roving paradigm) for the DFP project(Ece Kocagoncu,2017)
# ek390@cam.ac.uk

# Block 2

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

video { filename = "penguin2-1.xvid.avi"; 	height = 450; width = 800; end_time = 155000;} penguin21; 
video { filename = "penguin2-2.xvid.avi"; 	height = 450; width = 800; end_time = 156000;} penguin22; 

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
	video penguin21;
	time = 0;
	#port_code = 20;
	
	TEMPLATE "roving.tem" {
		soundfile condition trigger	;
		TEMPLATE "rov2-1.txt";
	};
};

trial {
	video penguin22;
	time = 0;
	#port_code = 20;
	
	TEMPLATE "roving.tem" {
		soundfile condition trigger	;
		TEMPLATE "rov2-2.txt";
	};
};

trial {
	trial_duration = forever;
	trial_type = specific_response;
	terminator_button = 2;
	
	picture {
		text {
			caption = "You have completed the task. \n Please have a short break now.";
			background_color = 200,200,200;
			font_color = 0,0,0;
			width = 700;
			height = 600;
		};
	x = 0; y = 0;
	};
};