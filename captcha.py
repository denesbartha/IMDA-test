import argparse
import logging

from PIL import Image


class Captcha(object):
    score_table = {
        26622703831098726513855: 'A',
        27008132336701494820644: 'B',
        18498956091371910939048: 'C',
        27007854359823311888232: 'D',
        17625899469123210706848: 'E',
        53281649195127969452892: 'F',
        18383990523184784126915: 'G',
        26640749417368155386724: 'H',
        18096974851160681907684: 'I',
        39351426763227391830204: 'J',
        27084881711340547886880: 'K',
        17626049865178828212667: 'L',
        26639989377891308108712: 'M',
        25760514696146198798335: 'N',
        30188127055152141518256: 'O',
        53281563160534943388286: 'P',
        17263341089396700500015: 'Q',
        26680850994944247235937: 'R',
        16580158695482559583472: 'S',
        43661474652606417174491: 'T',
        30188127044310298035038: 'U',
        43551287103958226465895: 'V',
        25329878814827491115112: 'W',
        26661261708197290581132: 'X',
        43661467064742537274946: 'Y',
        17624149399861213282502: 'Z',
        42436625011756130727132: '0',
        18096974570128686355849: '1',
        4613841854003088214530: '2',
        28384232741340936459703: '3',
        34757150346768713896989: '4',
        30190891455050210039639: '5',
        30188208218048391900037: '6',
        53260894319477455608789: '7',
        30188286929832080062717: '8',
        30200880193813367500759: '9'
    }

    def __init__(self):
        self.threshold = 60
        self.start_x = 5
        self.start_y = 11
        self.spacing = 1
        self.letter_width = 8
        self.letter_height = 10
        self.letter_cnt = 5

    @staticmethod
    def calculate_letter_score(img: Image, x1: int, y1: int, x2: int, y2: int) -> int:
        """Simple algorithm for calculating the score for a given area of the image. The algorithm
        takes the weighted sums for each line in the area. The weights are multiplied by powers of
        11. This creates a sequence where the sum uniquely identifies the contributing indices."""
        primes = [2, 3, 5, 7, 11, 13, 17, 19]
        score = 0
        for y in range(y1, y2):
            s = 0
            for x in range(x1, x2):
                s += img.getpixel((x, y)) * primes[x - x1]
            score += s * 11 ** y
        return score

    @staticmethod
    def find_best_match(score: int) -> str:
        """This algorithm returns the letter if there is an exact match, otherwise it searches
        the closest letter."""
        if score in Captcha.score_table:
            return Captcha.score_table[score]
        # otherwise find the closest number in score_table  arg_min_{letter} {score_table}
        return min(Captcha.score_table.items(), key=lambda x: abs(x[1] - score))[0]

    @staticmethod
    def get_image_data(image_path: str) -> Image:
        """Loads the image to the memory."""
        try:
            return Image.open(image_path)
        except:
            logging.error(f"The given file {image_path} could not be loaded...")

    @staticmethod
    def save_text_to_file(output_file_path: str, output_text: str) -> None:
        """Saves the result into the given file."""
        try:
            with open(output_file_path, "w") as f:
                f.write(f"{output_text}\n")
        except:
            logging.error(f"Could not save the file to the specified destination {output_text}...")

    def __call__(self, im_path: str, save_path: str):
        """
        Algo for inference
        args:
            im_path: .jpg image path to load and to infer
            save_path: output file path to save the one-line outcome
        """
        img = Captcha.get_image_data(im_path)
        if img is None:
            return

        # Convert the image to grayscale
        img = img.convert('L')
        # Apply a threshold to convert the image to binary
        img = img.point(lambda p: p > self.threshold)
        letters: list[str] = []
        for i in range(self.letter_cnt):
            score = Captcha.calculate_letter_score(
                img=img,
                x1=self.start_x + i * (self.letter_width + self.spacing),
                y1=self.start_y,
                x2=self.start_x + i * self.spacing + (i + 1) * self.letter_width,
                y2=self.start_y + self.letter_height
            )
            letters.append(Captcha.find_best_match(score))
        Captcha.save_text_to_file(save_path, "".join(letters))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Solution for the captcha problem")
    parser.add_argument("input", type=str, help="Specify the input jpeg file.")
    parser.add_argument("output", type=str, help="Specify th output txt file.")

    args = parser.parse_args()
    c = Captcha()
    c(im_path=args.input, save_path=args.output)
