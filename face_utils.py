import os
import cv2
import numpy as np

DATASET_DIR = "dataset"
MODEL_PATH = "trainer/trainer.yml"

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def get_face_id(student_id):
    return int(student_id) % 1000  # safe numeric hash

def capture_faces(student_id, subject, num_images=30):
    save_path = os.path.join(DATASET_DIR, subject, student_id)
    os.makedirs(save_path, exist_ok=True)

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    count = 0

    while True:
        ret, frame = cap.read()
        if not ret: break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            count += 1
            face_img = gray[y:y+h, x:x+w]
            file_path = os.path.join(save_path, f"{count}.jpg")
            cv2.imwrite(file_path, face_img)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        cv2.imshow("Capturing Faces", frame)
        if cv2.waitKey(1) & 0xFF == ord('q') or count >= num_images:
            break

    cap.release()
    cv2.destroyAllWindows()
    return count

def train_faces():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    faces, ids = [], []

    for subject in os.listdir(DATASET_DIR):
        subject_path = os.path.join(DATASET_DIR, subject)
        for student_id in os.listdir(subject_path):
            student_path = os.path.join(subject_path, student_id)
            face_id = get_face_id(student_id)
            for img_name in os.listdir(student_path):
                if img_name.endswith(".jpg"):
                    img_path = os.path.join(student_path, img_name)
                    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                    faces.append(img)
                    ids.append(face_id)

    recognizer.train(faces, np.array(ids))
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    recognizer.save(MODEL_PATH)
