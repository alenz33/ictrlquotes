
FILE=" \
int main(int argc, char **argv) \
{ \
	return 0; \
} \
"

all:
	@echo "I CANNOT support your lazyness! Do at least some tests with 'make test'!"

build_test_all_the_fancy_stuff:
	@echo $(FILE) > fancy.cpp
	g++ -std=c++0x -g -O0 -Wall  fancy.cpp -o magic
	@sleep 3
	g++ -std=c++0x -g -O0 -Wall  fancy.cpp -o magic
	@sleep 3
	
	@echo ""
	@echo "I compiled some highly advanced code and the code quality of this software seems to be very high!"
	@echo "It was even compiled twice to ensure consistent code quality!"
	
	@rm -f fancy.cpp magic

test_all_the_fancy_stuff: build_test_all_the_fancy_stuff

do_some_crazy_string_replacement_to_let_the_author_look_like_he_is_an_hardcore_c_programmer:
	@echo $(subst fancy,crazy,I am doing fancy stuff!)

test: do_some_crazy_string_replacement_to_let_the_author_look_like_he_is_an_hardcore_c_programmer test_all_the_fancy_stuff
