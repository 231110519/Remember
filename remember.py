import pygame
import random
import time
import speech_recognition as sr
import pyttsx3

pygame.init()
WIDTH, HEIGHT = 700, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🧠 Color Memory Game")

font = pygame.font.SysFont(None, 36)
BIG_FONT = pygame.font.SysFont(None, 48)
SMALL_FONT = pygame.font.SysFont(None, 24)

colors_dict = {
    "RED": (255, 0, 0),
    "GREEN": (0, 200, 0),
    "YELLOW": (255, 255, 0),
}

color_names = list(colors_dict.keys())

engine = pyttsx3.init()
def speak(text):
    engine.say(text)
    engine.runAndWait()

def draw_text_center(text, y, font=font, color=(0, 0, 0)):
    render = font.render(text, True, color)
    rect = render.get_rect(center=(WIDTH // 2, y))
    screen.blit(render, rect)

def show_colors_sequence(seq):
    box_size = 180
    box_x = (WIDTH - box_size) // 2
    box_y = (HEIGHT - box_size) // 2

    for color_name in seq:
        screen.fill((30, 30, 30))
        pygame.draw.rect(screen, colors_dict[color_name], (box_x, box_y, box_size, box_size), border_radius=20)
        pygame.display.flip()
        time.sleep(1.5)
        screen.fill((30, 30, 30))
        pygame.display.flip()
        time.sleep(0.5)

def listen_mode():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Please say the mode: normal, hard, or extreme.")
        print("Listening for mode command...")
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source, phrase_time_limit=4)
    try:
        command = r.recognize_google(audio).lower()
        print(f"You said: {command}")
        if "normal" in command:
            speak("Normal mode selected")
            return 3
        elif "hard" in command:
            speak("Hard mode selected")
            return 5
        elif "extreme" in command:
            speak("Extreme mode selected")
            return 25
        else:
            speak("Mode not recognized, please try again.")
            return None
    except sr.UnknownValueError:
        speak("Sorry, I did not understand. Please try again.")
        return None
    except sr.RequestError:
        speak("Failed to access speech recognition service.")
        return None

def mode_menu():
    while True:
        screen.fill((30, 30, 30))
        draw_text_center("🧠 COLOR MEMORY GAME", 60, BIG_FONT, (255, 215, 0))
        draw_text_center("Choose Mode:", 130, font, (200, 200, 200))
        draw_text_center("1. Normal (3 colors)", 170, font, (255, 100, 100))
        draw_text_center("2. Hard (3 colors)", 210, font, (100, 255, 100))
        draw_text_center("3. Extreme (3 colors)", 250, font, (255, 255, 100))
        draw_text_center("Press 1, 2, or 3 to start", 300, SMALL_FONT, (180, 180, 180))
        draw_text_center("Or press SPACE to select mode by voice", 330, SMALL_FONT, (180, 180, 180))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    speak("Normal mode selected")
                    return 3
                elif event.key == pygame.K_2:
                    speak("Hard mode selected")
                    return 5
                elif event.key == pygame.K_3:
                    speak("Extreme mode selected")
                    return 25
                elif event.key == pygame.K_SPACE:
                    mode_from_voice = listen_mode()
                    if mode_from_voice is not None:
                        return mode_from_voice

def draw_color_options(colors):
    box_size = 70
    spacing = 20
    total_width = len(colors) * box_size + (len(colors) - 1) * spacing
    start_x = (WIDTH - total_width) // 2
    y = HEIGHT - 110

    rects = []
    for i, cname in enumerate(colors):
        x = start_x + i * (box_size + spacing)
        rect = pygame.Rect(x, y, box_size, box_size)
        pygame.draw.rect(screen, colors_dict[cname], rect, border_radius=15)
        pygame.draw.rect(screen, (0, 0, 0), rect, 3, border_radius=15)
        rects.append((rect, cname))
    return rects

def draw_user_guesses(user_guesses):
    box_size = 60
    spacing = 10

    count = len(user_guesses)
    if count == 0:
        return []

    cols = 5
    rows = (count + cols - 1) // cols
    total_width = cols * box_size + (cols - 1) * spacing
    total_height = rows * box_size + (rows - 1) * spacing

    start_x = (WIDTH - total_width) // 2
    max_bottom = HEIGHT - 160
    start_y = max_bottom - total_height

    rects_with_x = []

    for i, cname in enumerate(user_guesses):
        row = i // cols
        col = i % cols
        x = start_x + col * (box_size + spacing)
        y = start_y + row * (box_size + spacing)
        color_rect = pygame.Rect(x, y, box_size, box_size)
        pygame.draw.rect(screen, colors_dict[cname], color_rect, border_radius=12)
        pygame.draw.rect(screen, (0, 0, 0), color_rect, 2, border_radius=12)

        x_size = 22
        x_rect = pygame.Rect(x + box_size - x_size, y, x_size, x_size)
        pygame.draw.rect(screen, (255, 80, 80), x_rect, border_radius=5)
        pygame.draw.line(screen, (0, 0, 0), (x_rect.left + 5, x_rect.top + 5), (x_rect.right - 5, x_rect.bottom - 5), 3)
        pygame.draw.line(screen, (0, 0, 0), (x_rect.left + 5, x_rect.bottom - 5), (x_rect.right - 5, x_rect.top + 5), 3)

        rects_with_x.append((color_rect, x_rect, i))

    return rects_with_x

def draw_button(text, rect, font=font, bg_color=(100, 180, 250), fg_color=(255, 255, 255)):
    pygame.draw.rect(screen, bg_color, rect, border_radius=12)
    pygame.draw.rect(screen, (0, 0, 0), rect, 3, border_radius=12)
    render = font.render(text, True, fg_color)
    text_rect = render.get_rect(center=rect.center)
    screen.blit(render, text_rect)

def main():
    while True:
        jumlah_urutan = mode_menu()
        if jumlah_urutan is None:
            break

        sequence = [random.choice(color_names) for _ in range(jumlah_urutan)]
        show_colors_sequence(sequence)

        pilihan_warna = color_names
        user_guesses = []
        result_state = None

        running = True
        while running:
            screen.fill((30, 30, 30))
            rects = draw_color_options(pilihan_warna)
            rects_user = draw_user_guesses(user_guesses)

            if result_state is None:
                draw_text_center("Click colors below to select", HEIGHT - 140, font, (200, 200, 200))
                draw_text_center("Click (X) on selected colors to remove", HEIGHT - 120, font, (200, 200, 200))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if result_state is None:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        for rect, cname in rects:
                            if rect.collidepoint(pos) and len(user_guesses) < jumlah_urutan:
                                user_guesses.append(cname)
                                break
                        for color_rect, x_rect, idx in rects_user:
                            if x_rect.collidepoint(pos) and 0 <= idx < len(user_guesses):
                                user_guesses.pop(idx)
                                break
                        if len(user_guesses) == jumlah_urutan:
                            if user_guesses == sequence:
                                result_state = 'win'
                                speak("Congratulations! You win.")
                            else:
                                result_state = 'lose'
                                speak("You lose! Try again.")
                else:
                    pass

            if result_state is not None:
                while True:
                    screen.fill((30, 30, 30))
                    if result_state == 'lose':
                        draw_text_center("Wrong! The correct sequence was:", 60, BIG_FONT, (255, 70, 70))
                        box_size = 50
                        spacing = 10
                        cols = 10
                        count = len(sequence)
                        rows = (count + cols - 1) // cols
                        total_width = cols * box_size + (cols - 1) * spacing
                        start_x = (WIDTH - total_width) // 2
                        y = 120
                        for i, cname in enumerate(sequence):
                            row = i // cols
                            col = i % cols
                            x = start_x + col * (box_size + spacing)
                            yy = y + row * (box_size + spacing)
                            pygame.draw.rect(screen, colors_dict[cname], (x, yy, box_size, box_size), border_radius=12)
                            pygame.draw.rect(screen, (0, 0, 0), (x, yy, box_size, box_size), 2, border_radius=12)
                    else:
                        draw_text_center("Congratulations! You Win!", HEIGHT // 2, BIG_FONT, (100, 255, 100))

                    btn_width, btn_height = 180, 50
                    btn_retry = pygame.Rect((WIDTH // 2 - btn_width - 20, HEIGHT - 100), (btn_width, btn_height))
                    btn_quit = pygame.Rect((WIDTH // 2 + 20, HEIGHT - 100), (btn_width, btn_height))

                    draw_button("Retry", btn_retry)
                    draw_button("Quit", btn_quit)

                    pygame.display.flip()

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            return
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            pos = pygame.mouse.get_pos()
                            if btn_retry.collidepoint(pos):
                                running = False
                                result_state = None
                                user_guesses.clear()
                                break
                            if btn_quit.collidepoint(pos):
                                return

                    if not running:
                        break

if __name__ == "__main__":
    main()
    pygame.quit()
