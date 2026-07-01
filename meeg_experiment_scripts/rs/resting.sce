#Resting state for the DFP project(Ece Kocagoncu,2017)


# TO-DO:
# Check that the devices and buttons are correct. Where is parallel port specified?
# Check that the timings are correct.
# Check that triggers are being sent.
# Is pulse_width needed?
# Customise logfile to include triggers and files.


#parameters
scenario = "Resting";
default_font_size = 24;
active_buttons = 2;
button_codes = 1,2;
default_background_color = 200,200,200;
default_font = "Arial";
default_text_color = 0,0,0;
write_codes = true; #send triggers
pulse_width = 50; #not sure about this
response_matching = simple_matching;
no_logfile = false;

begin;

#instructions
trial {
	trial_duration = forever;
	trial_type = first_response;
	
	picture {
		text {
			caption = "Today's tasks: \n\n Sound check   2 min   COMPLETE \n Resting eyes open  9 min   ... \n Resting eyes closed  9 min   ... \n Perceptual task   10 min   ... \n Watch documentary   15 min   ... \n Moon detection task   10 min   ... \n Pair learning task   3 min   ... \n  Circle detection task   25 min   ... \n\n Press button to continue.";
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
			caption = "In the next 9 min, we will do \n a recording as you rest. \n\n Please clear your mind, relax, and \n try not to think of anything in particular. \n Please stay awake and focus your \n eyes on the + at the centre. \n\n Press button to proceed.";
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

#resting state start
trial {
	trial_duration = 520000;
	trial_type = fixed;
	
	picture {
		background_color = 0,0,0;
		bitmap { filename = "fixation_MEG.bmp"; preload = true; width = 700; height = 524; }; 
		x = 0; y = 0;
	};
	port_code = 50;
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