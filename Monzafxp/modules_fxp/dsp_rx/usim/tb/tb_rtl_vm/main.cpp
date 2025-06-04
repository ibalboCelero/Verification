
#include <iostream>

#include "tb_rtl_vm.cpp"

int main(int argc, char *argv[])
{
    Root root;
    root.ProcessOptions(argc, argv);
    root.Run();
    return 0;
}
