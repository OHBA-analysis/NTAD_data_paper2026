# Sound test for the DFP project(Aya Ben Yakov & Ece Kocagoncu, 2017)
# ek390@cam.ac.uk

#parameters
scenario = "Sound_test";
default_font_size = 24;
active_buttons = 2;
button_codes = 1,2;
default_background_color = 128,128,128;
default_font = "Arial";
default_text_color = 0,0,0;
write_codes = false; #send triggers
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
Sound check   2 min  ...
Watch documentary   10 min  ...
Letter detection task   15 min  ...
Perceptual task   8 min  ...
Moon detection task   10 min  ...
Resting eyes open  5 min  ...
Resting eyes closed  5 min  ...\n
Press button to continue.";
			background_color = 128,128,128;
			font_color = 255,255,255;
			width = 700;
			height = 600;
		};
	x = 0; y = 0;
	};
} task_list;

trial {
	trial_duration = forever;
	trial_type = first_response;
	
	picture {
		text {
			caption = "We will start with a quick sound test \n to make sure that the \n earphones are working properly. \n\n There will be sounds coming to \n each ear separately of varying loudness. \n Please press the button \n when you hear a sound. \n\n Press button to proceed.";
			background_color = 200,200,200;
			font_color = 0,0,0;
			width = 700;
			height = 600;
		};
	x = 0; y = 0;
	};
} instructions_trial;

trial {
	trial_duration = 5000;
	trial_type = fixed;
	
	picture {
		text {
			caption = "Get ready";
			background_color = 200,200,200;
			font_color = 0,0,0;
			width = 700;
			height = 600;
		};
	x = 0; y = 0;
	};
} ready;

trial {
	trial_duration = forever;
	trial_type = specific_response;
	terminator_button = 2;
	
	picture {
		text {
			caption = "All done. \n Please have a short break now.";
			background_color = 200,200,200;
			font_color = 0,0,0;
			width = 700;
			height = 600;
		};
	x = 0; y = 0;
	};

} bye;

# sounds
array {
	TEMPLATE "sound_test_tem.tem" {
		ear db ;
		TEMPLATE "sound_attributes.txt";
	};
} sounds;


trial {
	trial_duration = stimuli_length;
	all_responses = true;
	stimulus_event {
		sound {wavefile { filename = "TestSound.wav"; };};
		time = 0;
		duration = 1000;
		target_button=1;
		code = "sound";
	} sound_event;
} sound_trial;

picture {
		background_color = 0,0,0;
		bitmap { filename = "fixation_MEG.bmp"; width = 1000; height = 750; }; 
		x = 0; y = 0;
} background_pic;


#######################################################################################

begin_pcl;

task_list.present();
instructions_trial.present();
ready.present();
background_pic.present();

int n_sounds = sounds.count();

# Open input file with durations and read into an array
input_file duration_file = new input_file;
array<int> durations[n_sounds];
duration_file.open("sound_duration.txt");

loop
	int i = 0
until
	i >= n_sounds
begin
	i = i + 1;
	durations[i] = duration_file.get_int();
end;
duration_file.close();

# Open input file with pan and read into an array
input_file pan_file = new input_file;
array<int> pan[n_sounds];
pan_file.open("sound_pan.txt");
loop
	int i = 0
until
	i >= n_sounds
begin
	i = i + 1;
	pan[i] = pan_file.get_int();
end;
pan_file.close();

# Open input file with attenuation and read into an array
input_file attenuation_file = new input_file;
array<double> attenuation[n_sounds];
attenuation_file.open("sound_attenuation.txt");
loop
	int i = 0
until
	i >= n_sounds
begin
	i = i + 1;
	attenuation[i] = attenuation_file.get_double();
end;
attenuation_file.close();

double max_attenuation_L = 0; 
double max_attenuation_R = 0; 

int clicks_before = 0;

loop
	int i = 0
until
	i >= 50
begin
	i = i + 1;
	sound_trial.set_duration(durations[i]+500);
	sound_event.set_stimulus(sounds[i]);
	sound_trial.present();
	
	stimulus_data last = stimulus_manager.last_stimulus_data();
	
	#####
	
	# If there was a response - check whether it's larger than current max attenuation (separately per ear)
	#int clicks_now = system_keyboard.keypress_count(); 
	
		if (last.type() == stimulus_hit && pan[i]==-1 && attenuation[i]>max_attenuation_L) then 
			max_attenuation_L = attenuation[i];	
			#clicks_before = clicks_now;
		elseif (last.type() == stimulus_hit && pan[i]==1 && attenuation[i]>max_attenuation_R) then 	
			max_attenuation_R = attenuation[i];	
			#clicks_before = clicks_now;
		end;
end;
#term.print("Clicks now: " + string(clicks_now) + "\nClicks before:" + string(clicks_before) + "\n");
term.print("Max Right: " + string(max_attenuation_R*100) + "\nMax Left: " + string(max_attenuation_L*100) + "\n");
bye.present();