
//init our variables
long max_delta;
long x_counter;
long y_counter;
bool x_can_step;
bool y_can_step;
int milli_delay;

void init_steppers()
{
	//turn them off to start.
	disable_steppers();
	
	//init our points.
	current_units.x = 0.0;
	current_units.y = 0.0;
	target_units.x = 0.0;
	target_units.y = 0.0;
	
	pinMode(X_STEP_PIN, OUTPUT);
	pinMode(X_DIR_PIN, OUTPUT);
	pinMode(X_ENABLE_PIN, OUTPUT);
	pinMode(X_MIN_PIN, INPUT_PULLUP);
	pinMode(X_MAX_PIN, INPUT_PULLUP);
	
	pinMode(Y_STEP_PIN, OUTPUT);
	pinMode(Y_DIR_PIN, OUTPUT);
	pinMode(Y_ENABLE_PIN, OUTPUT);
	pinMode(Y_MIN_PIN, INPUT_PULLUP);
	pinMode(Y_MAX_PIN, INPUT_PULLUP);

	digitalWrite(X_STEP_PIN, LOW);
	digitalWrite(X_DIR_PIN, LOW);
	
	digitalWrite(Y_STEP_PIN, LOW);
	digitalWrite(Y_DIR_PIN, LOW);
	
	
	//figure our stuff.
	calculate_deltas();
  	goto_machine_zero();
}

void goto_machine_zero()
{
  Serial.println("init");
  move_to_max(X_MIN_PIN, X_STEP_PIN, X_DIR_PIN, 0);
  move_to_max(Y_MIN_PIN, Y_STEP_PIN, Y_DIR_PIN, 0);
  Serial.println("ok");
}

void move_to_max(int limiter_pin, int stepper_pin, int stepper_dir_pin,int dir)
{
  /* Moves to the maximum possible position
  */
  while(can_step(limiter_pin, limiter_pin, 0, 1, dir)){
    do_step(stepper_pin, stepper_dir_pin, 0);
    // Moving 3 steps at the time as once was a bit slow. 
    // Note: This could be a very bad idea!
    do_step(stepper_pin, stepper_dir_pin, 0);
    do_step(stepper_pin, stepper_dir_pin, 0);
    delay(1);
  }
  // slowly back unitl pin is released
  while(!can_step(limiter_pin, limiter_pin, 0, 1, dir)){
    do_step(stepper_pin, stepper_dir_pin, 1);
    delay(100);
  }
}

void dda_move(long micro_delay)
{
	//enable our steppers
	digitalWrite(X_ENABLE_PIN, HIGH);
	digitalWrite(Y_ENABLE_PIN, HIGH);
	
	//figure out our deltas
	max_delta = max(delta_steps.x, delta_steps.y);

	//init stuff.
	long x_counter = -max_delta/2;
	long y_counter = -max_delta/2;
	
	//our step flags
	bool x_can_step = 0;
	bool y_can_step = 0;
	
	if (micro_delay >= 16383)
		milli_delay = micro_delay / 1000;
	else
		milli_delay = 0;

	//do our DDA line!
	do
	{
		x_can_step = can_step(X_MIN_PIN, X_MAX_PIN, current_steps.x, target_steps.x, x_direction);
		y_can_step = can_step(Y_MIN_PIN, Y_MAX_PIN, current_steps.y, target_steps.y, y_direction);

		if (x_can_step)
		{
			x_counter += delta_steps.x;
			
			if (x_counter > 0)
			{
				do_step(X_STEP_PIN, X_DIR_PIN, x_direction);
				x_counter -= max_delta;
				
				if (x_direction)
					current_steps.x++;
				else
					current_steps.x--;
			}
		}

		if (y_can_step)
		{
			y_counter += delta_steps.y;
			
			if (y_counter > 0)
			{
				do_step(Y_STEP_PIN, Y_DIR_PIN, y_direction);
				y_counter -= max_delta;

				if (y_direction)
					current_steps.y++;
				else
					current_steps.y--;
			}
		}
		
		//wait for next step.
		if (milli_delay > 0)
			delay(milli_delay);			
		else
			delayMicroseconds(micro_delay);
	}
	while (x_can_step || y_can_step);
	
	//set our points to be the same
	current_units.x = target_units.x;
	current_units.y = target_units.y;
	calculate_deltas();
}

bool can_step(byte min_pin, byte max_pin, long current, long target, byte direction)
{
	//stop us if we're on target
	if (target == current)
		return false;
	//stop us if we're at home and still going 
	else if (read_switch(min_pin) && !direction)
		return false;
	//stop us if we're at max and still going
	else if (read_switch(max_pin) && direction)
		return false;

	//default to being able to step
	return true;
}

void do_step(byte pinA, byte pinB, byte dir)
{
        switch (dir << 2 | digitalRead(pinA) << 1 | digitalRead(pinB)) {
            case 0: /* 0 00 -> 10 */
            case 5: /* 1 01 -> 11 */
                digitalWrite(pinA, HIGH);
                break;
            case 1: /* 0 01 -> 00 */
            case 7: /* 1 11 -> 10 */
                digitalWrite(pinB, LOW);
                break;
            case 2: /* 0 10 -> 11 */
            case 4: /* 1 00 -> 01 */   
                digitalWrite(pinB, HIGH);
                break;
            case 3: /* 0 11 -> 01 */
            case 6: /* 1 10 -> 00 */
                digitalWrite(pinA, LOW);
                break;
        }
	delayMicroseconds(5);
}


bool read_switch(byte pin)
{
	//dual read as crude debounce
	
	if ( SENSORS_INVERTING )
		return !digitalRead(pin) && !digitalRead(pin);
	else
		return digitalRead(pin) && digitalRead(pin);
}

long to_steps(float steps_per_unit, float units)
{
	return steps_per_unit * units;
}

void set_target(float x, float y)
{
	target_units.x = x;
	target_units.y = y;
	
	calculate_deltas();
}

void set_position(float x, float y)
{
	current_units.x = x;
	current_units.y = y;
	
	calculate_deltas();
}

void calculate_deltas()
{
	//figure our deltas.
	delta_units.x = abs(target_units.x - current_units.x);
	delta_units.y = abs(target_units.y - current_units.y);
				
	//set our steps current, target, and delta
	current_steps.x = to_steps(x_units, current_units.x);
	current_steps.y = to_steps(y_units, current_units.y);

	target_steps.x = to_steps(x_units, target_units.x);
	target_steps.y = to_steps(y_units, target_units.y);

	delta_steps.x = abs(target_steps.x - current_steps.x);
	delta_steps.y = abs(target_steps.y - current_steps.y);
	
	//what is our direction
	x_direction = (target_units.x >= current_units.x);
	y_direction = (target_units.y >= current_units.y);

	//set our direction pins as well
	digitalWrite(X_DIR_PIN, x_direction);
	digitalWrite(Y_DIR_PIN, y_direction);
}


long calculate_feedrate_delay(float feedrate)
{
	//how long is our line length?
	float distance = sqrt(delta_units.x*delta_units.x + delta_units.y*delta_units.y + delta_units.z*delta_units.z);
	long master_steps = 0;
	
	//find the dominant axis.
	master_steps = max(delta_steps.x, delta_steps.y);

	//calculate delay between steps in microseconds.  this is sort of tricky, but not too bad.
	//the formula has been condensed to save space.  here it is in english:
	// distance / feedrate * 60000000.0 = move duration in microseconds
	// move duration / master_steps = time between steps for master axis.

	return ((distance * 60000000.0) / feedrate) / master_steps;	
}

long getMaxSpeed()
{
	return calculate_feedrate_delay(FAST_XY_FEEDRATE);
}

void disable_steppers()
{
	//enable our steppers
	digitalWrite(X_ENABLE_PIN, LOW);
	digitalWrite(Y_ENABLE_PIN, LOW);
}
