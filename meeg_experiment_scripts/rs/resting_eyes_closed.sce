#Resting state eyes closed for the DFP project(Ece Kocagoncu,2017)
#ek390@cam.ac.uk

#parameters
scenario = "Resting";
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
Perceptual task   8 min  COMPLETED
Moon detection task   10 min  COMPLETED
Resting eyes open  5 min  COMPLETED
Resting eyes closed  5 min  ...\n
Press button to continue.";
			background_color = 200,200,200;
			font_color = 0,0,0;
			width = 700;
			height = 600;
		};
	x = 0; y = 0;
	};
}trl_start;


trial {
	trial_duration = forever;
	trial_type = first_response;
	
	picture {
		text {
			caption = "In the next 5 min, we will do \n a recording as you rest. \n\n Please clear your mind, relax, and \n try not to think of anything in particular. \n Please close your eyes but do not fall asleep. \n\n Press button to proceed.";
			background_color = 200,200,200;
			font_color = 0,0,0;
			width = 700;
			height = 600;
		};
	x = 0; y = 0;
	};
}trl_inst;


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
}trl_hpi;

trial {
	trial_duration = 3000;
	trial_type = fixed;
	
	picture {
		text {
			caption = "We will let you know when 5 min is up.\n \n Please close your eyes";
			background_color = 200,200,200;
			font_color = 0,0,0;
			width = 700;
			height = 600;
		};
	x = 0; y = 0;
	};
}trl_rest_inst;

#resting state start
trial {
	trial_duration = 330000;
	trial_type = fixed;
	
	picture {
		background_color = 0,0,0;
	};
	port_code = 50;
}trl_rest;


# more instructions
trial {
	trial_duration = forever;
	trial_type = specific_response;
	terminator_button = 2;
	
	picture {
		text {
			caption = "You have completed the experiment! :) \n\n Thank you for your participation!";
			background_color = 200,200,200;
			font_color = 0,0,0;
			width = 700;
			height = 600;
		};
	x = 0; y = 0;
	};
}trl_finish;

begin_pcl;
eye_tracker eye = new eye_tracker("PresLink");
eye.start_tracking();

string edf_name = "eyetest";
string edf_arg = "open_edf_file";
eye.set_parameter(edf_arg,edf_name);

trl_start.present();
trl_inst.present();

eye.set_recording(true);
trl_hpi.present();

trl_rest_inst.present();
trl_rest.present();

trl_finish.present();

# Logfile is initially stored on eye-tracker
# Now transfer to simulus PC
eye.set_parameter("get_edf_file", "C:\\Users\\wayne\\Desktop\\Experiments\\SHINE\\6-Resting_state_ET\\logfiles\\eyelink_RSC.edf");
eye.stop_tracking();