def generate_function(num_args, num_grid_args):
    start_function = """
static double integrand_%i_%i(double x, void * vp){
    params * p = (params *)vp;
    return p->func(
        x"""

    end_function = """
    );
}
"""
    base_args = ",\n\t\tp->args[{}]"
    grid_args = ",\n\t\tp->grid_args[{}]"

    func = start_function%(num_args, num_grid_args)
    for i in range(num_grid_args):
        func += grid_args.format(i)

    for i in range(num_args):
        func += base_args.format(i)

    func += end_function

    return func


def generate_integrands_header():
    header = """#ifndef INTEGRANDS
#define INTEGRANDS

typedef double (*integrand)(double, ...);
typedef double (*integrand_wrapper)(double, void *);

typedef struct{
    double * args;
    double * grid_args;
    integrand func;
} params;
"""

    num_args = 15
    num_grid_args = 15
    for i in range(num_args):
        for j in range(num_grid_args):
            header += generate_function(i, j)

    header += "\nintegrand_wrapper integrand_functions[%i][%i] = {\n"%(num_args, num_grid_args)
    for i in range(num_args):
        header += "\t{ integrand_%i_%i, "%(i, 0)

        for j in range(1, num_grid_args - 1):
            header += "integrand_%i_%i, "%(i, j)

        header += "integrand_%i_%i },\n"%(i, num_grid_args - 1)

    header += "};"


    header += "\n\n#endif"

    with open("integrands.h", "w") as f:
        f.write(header)

generate_integrands_header()
