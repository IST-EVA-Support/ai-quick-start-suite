import cv2

points_list = []

def click_event(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        #print('(', x, ', ', y, ')')
        points_list.append((x, y))
 
        cv2.putText(img_paint, 
                    '(' + str(x) + ', ' + str(y) + ')', 
                    (x, y), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        cv2.circle(img_paint, (x, y), 3, (0, 0, 255), 3)
        n = len(points_list)
        if n > 1:
            p1 = points_list[n - 1]
            p2 = points_list[n - 2]
            cv2.line(img_paint, p1, p2,  (0, 128, 255), 2)
        cv2.imshow('image', img_paint)
     
    if event==cv2.EVENT_RBUTTONDOWN:
        n = len(points_list)
        if n > 1:
            p1 = points_list[n - 1]
            p2 = points_list[0]
            cv2.line(img_paint, p1, p2,  (0, 128, 255), 2)
        cv2.imshow('image', img_paint)
        
        height, width, channels = img.shape
        f = open('area.txt', 'w')
        for point in points_list:
            norm_x = float(point[0]) / width
            norm_y = float(point[1]) / height
            f.write(str(norm_x) + ',' + str(norm_y) + '\n')
        f.close()
            
        if n > 0:
            del points_list[:] 


if __name__=="__main__":
 
    img = cv2.imread('test.jpg', 1)
    img_paint = img.copy()
    cv2.imshow('image', img_paint)
 
    cv2.setMouseCallback('image', click_event)
 
    # wait for a ESC key to be pressed to exit or ctrl to clean
    while True:
        key = cv2.waitKey(0)
        print(key)
        if key == 27 or key == -1:
            break;
        elif key == 227:
            img_paint = img.copy()
            if len(points_list) > 0:
                del points_list[:]
            cv2.imshow('image', img_paint)
 
    cv2.destroyAllWindows()
