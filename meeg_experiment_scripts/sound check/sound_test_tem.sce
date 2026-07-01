#Sound test template (Ece Kocagoncu,2017)

#trial structure

trial {
	trial_duration = $trdur;
   trial_type = fixed;
   all_responses = false;

	sound beep;
	time = 0;
	code = "sound";
	duration = 1000;
	pan = $ear;
	attenuation = $db;
};

