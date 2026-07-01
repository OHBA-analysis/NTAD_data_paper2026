#Visual Auditory Oddball task for the DFP project(Ece Kocagoncu,2017)
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
	bitmap { filename = "a.bmp";  preload = true; width = 960; height = 720; }; 
	x = 0; y = 0;
} a;


#STD
sound { wavefile { filename = "aud17.wav"; preload = true; }; } aud1;
sound { wavefile { filename = "aud13.wav"; preload = true; }; } aud4;
sound { wavefile { filename = "aud6.wav"; preload = true; }; } aud3;
sound { wavefile { filename = "aud18.wav"; preload = true; }; } aud2;

#ND
sound { wavefile { filename = "aud4.wav"; preload = true; }; } aud5;
sound { wavefile { filename = "aud3.wav"; preload = true; }; } aud6;
sound { wavefile { filename = "aud5.wav"; preload = true; }; } aud7;
sound { wavefile { filename = "aud8.wav"; preload = true; }; } aud8;

sound { wavefile { filename = "silence.wav"; preload = true; }; } silence;


trial {
	trial_duration = forever;
	trial_type = first_response;
	
	picture {
		text {
			caption = "Now we are moving onto the task. \n\n In the next 14 min you \n will see the same images followed \n by some sounds. \n\n Please press the button \n  when you see the letter a. \n\n Press button to proceed.";
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


# task trial list

TEMPLATE "vao_train.tem" {
	trdur picfile condition trigger soundfile crossdur	soundtrigger;
	TEMPLATE "vab2_task_trials_b1.txt";
};

trial {
	trial_duration = forever;
	trial_type = first_response;
	
	picture {
		text {
			caption = "You are half way through \n\n A short break?";
			width = 700;
			height = 600;
		};
	x = 0; y = 0;
	};
};

TEMPLATE "vao_train.tem" {
	trdur picfile condition trigger soundfile crossdur	soundtrigger;
	TEMPLATE "vab2_task_trials_b2.txt";
};


# more instructions
trial {
	trial_duration = forever;
	trial_type = specific_response;
	terminator_button = 2;
	
	picture {
		text {
			caption = "Now we will quickly repeat the previous test. \n\n I'm going to play you a sound. \n You will then have to decide \n which of the four shapes on the screen, \n the sound was paired with more often, \n by saying top, bottom, left or right. \n\n Ready? ";
			width = 700;
			height = 600;
		};
	x = 0; y = 0;
	};
};

# test round 2

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

# more instructions
trial {
	trial_duration = forever;
	trial_type = specific_response;
	terminator_button = 2;
	
	picture {
		text {
			caption = "You have completed the task. :) \n\n Please take a short break now.";
			width = 700;
			height = 600;
		};
	x = 0; y = 0;
	};
};