# Mismatch negativity task (Roving paradigm) for the DFP project(Ece Kocagoncu,2017)
# ek390@cam.ac.uk

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

video { filename = "penguin1-1.xvid.avi"; 	height = 450; width = 800; end_time = 154000;} penguin11; #likes xvid so much
video { filename = "penguin1-2.xvid.avi"; 	height = 450; width = 800; end_time = 158000;} penguin12; 
video { filename = "penguin2-1.xvid.avi"; 	height = 450; width = 800; end_time = 155000;} penguin21; 
video { filename = "penguin2-2.xvid.avi"; 	height = 450; width = 800; end_time = 156000;} penguin22; 
video { filename = "penguin3-1.xvid.avi"; 	height = 450; width = 800; end_time = 154500;} penguin31;
video { filename = "penguin3-2.xvid.avi"; 	height = 450; width = 800; end_time = 156500;} penguin32; 

#instructions
trial {
	trial_duration = forever;
	trial_type = first_response;
	
	picture {
		text {
			caption = "Today's tasks: \n\n Sound check   2 min   COMPLETE \n Resting eyes open  9 min   COMPLETE \n Resting eyes closed  9 min   COMPLETE \n Perceptual task   10 min   COMPLETE \n Watch documentary   15 min   ... \n Moon detection task   10 min   ... \n Pair learning task   3 min   ... \n  Circle detection task   25 min   ... \n\n Press button to continue.";
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
			caption = "In the next 15 min, you will \n be watch a short clip from a \n nature documentary. \n\n As you watch you will hear \n sounds in the background. Please \n ignore them, just relax and \n enjoy the movie. \n\n Press button to proceed.";
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
	port_code = 20;
	
	TEMPLATE "roving.tem" {
		soundfile condition trigger	;
		TEMPLATE "rov1-1.txt";
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
	video penguin12;
	time = 0;
	port_code = 20;
	
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
			caption = "You have completed 1 of 3 parts. \n Please have a short break now.";
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
	video penguin21;
	time = 0;
	port_code = 20;
	
	TEMPLATE "roving.tem" {
		soundfile condition trigger	;
		TEMPLATE "rov2-1.txt";
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
	video penguin22;
	time = 0;
	port_code = 20;
	
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
			caption = "You have completed 2 of 3 parts. \n Please have a short break now.";
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
	video penguin31;
	time = 0;
	port_code = 20;
	
	TEMPLATE "roving.tem" {
		soundfile condition trigger	;
		TEMPLATE "rov3-1.txt";
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
	video penguin32;
	time = 0;
	port_code = 20;
	
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