begin;

trial {
	picture {
		box { height = 10; width = 10; color = 255,0,0; };
		x = 0; y = 0;	
	} pic1;
	duration = 2000;
}trial1;

trial {
	picture {
		box { height = 10; width = 10; color = 255,0,0; };
		x = 120; y = 0;
	} pic2;
	duration = 3000;
}trial2;

trial {
	picture {
		box { height = 10; width = 10; color = 255,0,0; };
		x = 0; y = 120;
	} pic3;
	duration = 2000;
}trial3;

trial {
	picture {
		box { height = 10; width = 10; color = 255,0,0; };
		x = -120; y = 0;
	} pic4;
	duration = 2000;
}trial4;

trial {
	picture {
		box { height = 10; width = 10; color = 255,0,0; };
		x = 0; y = -120;
	} pic5;
	duration = 2000;
}trial5;

begin_pcl;
eye_tracker eye = new eye_tracker("PresLink");
eye.start_tracking();

string edf_name = "eyetest";
string edf_arg = "open_edf_file";
eye.set_parameter(edf_arg,edf_name);

#eye.calibrate(et_calibrate_default,0.0,0.0,0.0);

eye.set_recording(true);

trial1.present();

# Lap 1
trial2.present();
trial3.present();
trial4.present();
trial5.present();

# Lap 2
trial2.present();
trial3.present();
trial4.present();
trial5.present();

# Logfile is initially stored on eye-tracker
# Now transfer to simulus PC
eye.set_parameter("get_edf_file","E:\\Experiments\\NTAD\\EyeLinker\\logfiles\\eyelink_test.edf");
eye.stop_tracking();