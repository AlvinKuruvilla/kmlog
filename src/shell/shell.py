# Copyright 2022, Alvin Kuruvilla <alvineasokuruvilla@gmail.com>, Dr. Rajesh Kumar <Rajesh.Kumar@hofstra.edu>

# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

from base.displayer import km_prompt
import cmd


class Shell(cmd.Cmd):
    FRIENDS = ["Alice", "Adam", "Barbara", "Bob"]
    prompt = km_prompt("")

    def do_greet(self, person):
        "Greet the person"
        if person and person in self.FRIENDS:
            greeting = "hi, %s!" % person
        elif person:
            greeting = "hello, " + person
        else:
            greeting = "hello"
        print(greeting)

    def complete_greet(self, text, line, begidx, endidx):
        if not text:
            completions = self.FRIENDS[:]
        else:
            completions = [f for f in self.FRIENDS if f.startswith(text)]
        return completions

    def do_EOF(self, line):
        return True


if __name__ == "__main__":
    Shell().cmdloop()
