#Visual Auditory Oddball Pilot task for the DFP project(Ece Kocagoncu,2017)
#ek390@cam.ac.uk

#parameters
scenario = "VABv2";
default_font_size = 24;
active_buttons = 2;
button_codes = 1,2;
default_background_color = 217,217,217;
default_font = "Arial";
default_text_color = 50,50,50;
write_codes = true; #send triggers
pulse_width = 50; #not sure about this
response_matching = simple_matching;
no_logfile = false;

begin;

#objects
picture {
	bitmap { filename = "Im30.bmp";  preload = true; width = 960; height = 720; }; 
	x = 0; y = 0;
} im1;

picture {
	bitmap { filename = "Im32.bmp";  preload = true; width = 960; height = 720; }; 
	x = 0; y = 0;
} im2;

picture {
	bitmap { filename = "Im34.bmp"; preload = true; width = 960; height = 720; }; 
	x = 0; y = 0;
} im3;

picture {
	bitmap { filename = "Im35.bmp";  preload = true; width = 960;  height = 720; };
	x = 0; y = 0;
} im4;

picture {
		text {
			caption = "+";
			width = 700;
			height = 600;
		};
x = 0; y = 0;
} cross;

#STD
sound { wavefile { filename = "aud17.wav"; preload = true; }; } aud1;
sound { wavefile { filename = "aud13.wav"; preload = true; }; } aud4;
sound { wavefile { filename = "aud6.wav"; preload = true; }; } aud3;
sound { wavefile { filename = "aud18.wav"; preload = true; }; } aud2;
sound { wavefile { filename = "silence.wav"; preload = true; }; } silence;


trial {
	trial_duration = forever;
	trial_type = first_response;
	
	picture {
		text {
			caption = "
Today's tasks:\n
Sound check   2 min  COMPLETED
Watch documentary   10 min  COMPLETED
Letter detection task   15 min  ...
Perceptual task   8 min   ...
Moon detection task   10 min   ...
Resting eyes open  5 min   ...
Resting eyes closed  5 min  ...\n
Press button to continue.";
			background_color = 217,217,217;
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
			caption = "In the next 3 min, you are going \n to see some shapes followed \n by some sounds.\n\n Please try to remember which \n shape is paired with which sound. \n I will be asking you at the end. \n\n Press button to proceed.";
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
			width = 700;
			height = 600;
		};
	x = 0; y = 0;
	};
};

# training trial list

TEMPLATE "vao_train.tem" {
	trdur picfile condition trigger soundfile crossdur	soundtrigger;
	TEMPLATE "vab2_training_trials.txt";
};

# more instructions
trial {
	trial_duration = forever;
	trial_type = specific_response;
	terminator_button = 2;
	
	picture {
		text {
			caption = "You have completed the training! :) \n\n Now I'm going to play you a sound. \n\n You will then have to decide \n which of the four shapes on the screen, \n the sound was paired with, \n by saying top, bottom, left or right. \n\n Ready? ";
			width = 700;
			height = 600;
		};
	x = 0; y = 0;
	};
};


# test round

TEMPLATE "vao_test.tem" {
	soundfile;
	aud1 ;
	aud2 ;
	aud4 ;
	aud3 ;	
	aud1 ;
	aud2 ;
	aud4 ;
	aud3 ;
	aud2 ;
	aud1 ;
}; 
