
FILE=" \
int main(int argc, char **argv) \
{ \
	return 0; \
} \
"

all:
	@echo $(FILE) > fancy.cpp
	g++ -std=c++0x -g -O0 -Wall  fancy.cpp -o magic
	@sleep 3
	g++ -std=c++0x -g -O0 -Wall  fancy.cpp -o magic
	@sleep 3
	
	@echo ""
	@echo "I compiled some highly advanced code and the code quality of this software seems to be very high!"
	@echo "It was even compiled twice to ensure consistent code quality!"
	
	@rm -f fancy.cpp magic
