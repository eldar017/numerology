from datetime import datetime

# Assuming the date of birth is in the format "DD/MM/YYYY"
date_of_birth = "04/09/1990"

# Parse the date of birth string into a datetime object
dob = datetime.strptime(date_of_birth, "%d/%m/%Y")

# Get the current date
current_date = datetime.now()

# Compare the month and day of the date of birth with the current month and day
if (dob.month, dob.day) <= (current_date.month, current_date.day):
    # The person has already celebrated their birthday this year
    actual_years = current_date.year - dob.year
    print("Celebrated birthday in", current_date.year, "(", actual_years, "years old)")
else:
    # The person has not celebrated their birthday this year yet
    last_years = current_date.year - 1 - dob.year
    print("Did not celebrate birthday in", current_date.year, "(", last_years, "years old)")

    font_face = cv2.FONT_HERSHEY_COMPLEX
    # font_face = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX
    font_scale = 0.55
    font_thickness = 1
    image = cv2.imread("background.jpg")

    #   הוספת הטקסטים לתמונה של מפה נומרולוגית
    parameters = [calHead, calHand, calHand, calLegs, calRightLeg, calLeftLeg, calHearth, calSpirala]
    locations = [(290, 38), (509, 408), (70, 410), (283, 727), (540, 726), (25, 726), (320, 215), (300, 298)]
    color = (100, 255, 0)  # צבע שחור

    for parameter, location in zip(parameters, locations):
        text = str(parameter)
        position = location
        cv2.putText(image, text, position, font_face, font_scale, color, font_thickness, cv2.LINE_AA, False)
    cv2.imwrite("static/param_table.jpg", cv_image)