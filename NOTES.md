# What I checked, and what the agent got wrong

Write this yourself, in your own words. It is the part of the repo that proves the work is yours.

## What the agent got wrong
The agent said there was no need to run the tests because Python was not installed. However, the task explicitly required the tests to be run before accepting the work. I caught this because the prompt said, “Do not tell me it is done until you have actually run the tests.” So I did not accept its analysis as proof that the tests pass

## What I checked before I accepted its work
I checked the agent's explanation against the requirements. I verified that the wear bug comes from using // instead of /, and that the 80% warning threshold and 15,000 km service interval must remain unchanged. I also checked that the missing last_service_km case needs to be handled without treating it as zero. I did not accept the work yet because the agent had not actually run the tests.

## What the data actually said
The data showed which factors were associated with breakdowns, while one factor that seemed important at first did not actually predict breakdowns. I learned that the actual data was more reliable than assumptions based on what seemed obvious.