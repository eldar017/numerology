import cv2
from matplotlib import pyplot as plt

# פונקציה המתרחשת בעת לחיצה על התמונה
def onclick(event):
    # בדוק אם הלחיצה היא על התמונה
    if event.inaxes == ax:
        # הוסף את המיקום לרשימות
        x.append(event.xdata)
        y.append(event.ydata)
        # סמן את הנקודה על התמונה
        ax.plot(event.xdata, event.ydata, 'ro')
        plt.draw()

# טען את התמונה
image = cv2.imread('table.jpg')

# הצג את התמונה בעזרת Matplotlib
fig, ax = plt.subplots()
ax.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.title('Click on the image to mark locations')

# רשימות לשמירת מיקומים
x = []
y = []

# קרא את הפונקציה onclick כאשר יש לחיצה על התמונה
fig.canvas.mpl_connect('button_press_event', onclick)

# הצג את החלון
plt.show()

# עכשיו תוכל להשתמש ברשימות x ו-y שמכילות את המיקומים שנסמנו על התמונה


