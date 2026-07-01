# Unimodal Pilot Audiovisual task for the DFP project(Ece Kocagoncu,2017)
#ek390@cam.ac.uk

#parameters
scenario = "UnimodalAV";
default_font_size = 24;
active_buttons = 2;
button_codes = 1,2;
default_background_color = 128,128,128;
default_font = "Arial";
default_text_color = 255,255,255;
write_codes = true; #send triggers
pulse_width = 20; 
response_matching = simple_matching;
no_logfile = false;

begin;

#objects
picture {
	background_color = 128,128,128;
	bitmap { filename = "board.bmp"; preload = true; width = 960; height = 720; }; #checkerboard_MEG.bmp 768x768
	x = 0; y = 0;
} board; 

picture {
	background_color = 128,128,128;
	bitmap { filename = "grating.bmp"; preload = true; width = 960; height = 720; }; #checkerboard_MEG.bmp
	x = 0; y = 0;
} grating;

picture {
	background_color = 128,128,128;
	bitmap { filename = "dot.bmp"; preload = true; width = 960; height = 720; }; #checkerboard_MEG.bmp
	x = 0; y = 0;
} dot;

sound { wavefile { filename = "tone_300.wav"; preload = true; }; } t300;
sound { wavefile { filename = "tone_600.wav"; preload = true; }; } t600;
sound { wavefile { filename = "tone_1200.wav"; preload = true; }; } t1200;
sound { wavefile { filename = "silence.wav"; preload = true; }; } silence;

#instructions

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
Perceptual task   8 min   ...
Moon detection task   10 min   ...
Resting eyes open  5 min   ...
Resting eyes closed  5 min  ...\n
Press button to continue.";
			background_color = 128,128,128;
			font_color = 255,255,255;
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
			caption = "In the next 8 min, you will be \n seeing some shapes and listening to sounds. \n\n Please focus your eyes on the \n red dot at the centre. \n\n When you see or hear something, \n press the button as quickly as you can. \n\n Press button to proceed.";
			background_color = 128,128,128;
			font_color = 255,255,255;
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
			caption = "We will start with a short \n practice, so that you can \n get used to the task. \n\n Press button to proceed.";
			background_color = 128,128,128;
			font_color = 255,255,255;
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
			background_color = 128,128,128;
			font_color = 255,255,255;
			width = 700;
			height = 600;
		};
	x = 0; y = 0;
	};
};

#practice trial list
TEMPLATE "avtask.tem" {
	trdur picfile condition trigger soundfile crossdur	picdur;
	TEMPLATE "unimodalav_practice_trials.txt";
};


# more instructions
trial {
	trial_duration = forever;
	trial_type = specific_response;
	terminator_button = 2;
	
	picture {
		text {
			caption = "Is everything clear?";
			background_color = 128,128,128;
			font_color = 255,255,255;
			width = 700;
			height = 600;
		};
	x = 0; y = 0;
	};
};

trial {
	trial_duration = 3000;
   trial_type = fixed;
   all_responses = false;
	
	picture dot;
	time = 0;
};


TEMPLATE "avtask.tem" {
	trdur picfile condition trigger soundfile crossdur	picdur;	
	TEMPLATE "unimodalav_task_trials.txt";
};

# more instructions
trial {
	trial_duration = forever;
	trial_type = specific_response;
	terminator_button = 2;
	
	picture {
		text {
			caption = "You have completed the task! :) \n\n Please have a short break now.";
			background_color = 128,128,128;
			font_color = 255,255,255;
			width = 700;
			height = 600;
		};
	x = 0; y = 0;
	};
};