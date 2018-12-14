#include <stdlib.h>
#include <stdio.h>
#include <math.h> // required for fabs()
#include <gsl/gsl_integration.h>
#include <time.h>
#include <omp.h>

typedef double (*integrand)(double, ...);

typedef struct{
    double * args;
    integrand func;
} params;

static double integrand_6(double x, void * vp){
    params * p = (params *)vp;
    return p->func(x, p->args[0], p->args[1], p->args[2], p->args[3], p->args[4],
                   p->args[5]);
}

static double integrand_7(double x, void * vp){
    params * p = (params *)vp;
    return p->func(x, p->args[0], p->args[1], p->args[2], p->args[3], p->args[4],
                   p->args[5], p->args[6]);
}

void _quad(int num_args, void * p, double * result, double * error){
    gsl_integration_workspace * w = gsl_integration_workspace_alloc (50);

    gsl_function gfunc;
    if (num_args == 6)
        gfunc.function = integrand_6;
    if (num_args == 7)
        gfunc.function = integrand_7;
    gfunc.params = p;

    gsl_integration_qags(&gfunc, 0, 1, 1e-7, 1e-7, 50, w, result, error);
    gsl_integration_workspace_free(w);
}

void _quad_grid(int num_args, params ps, int num, double * grid1,
        double * grid2, double * result, double * error){

    gsl_integration_workspace * w = gsl_integration_workspace_alloc(50);
    gsl_function gfunc;
    gfunc.function = integrand_6;
    gfunc.params = (void *)&ps;

    for(int i=0; i<num; i++){
        ps.args[0] = grid1[i];
        ps.args[1] = grid2[i];
        gsl_integration_qags(&gfunc, 0, 1, 1e-5, 1e-5, 50, w, &result[i], &error[i]);
    }

    gsl_integration_workspace_free(w);
}

void _quad_grid_parallel(int num_args, params ps, int num, double * grid1,
        double * grid2, double * result, double * error){
    omp_set_num_threads(1);
    #pragma omp parallel firstprivate(ps)
    {
    gsl_integration_workspace * w = gsl_integration_workspace_alloc(50);
    gsl_function gfunc;
    gfunc.function = integrand_6;
    gfunc.params = (void *)&ps;

    #pragma omp for schedule(static, 200)
    for(int i=0; i<num; i++){
        ps.args[0] = grid1[i];
        ps.args[1] = grid2[i];
        gsl_integration_qags(&gfunc, 0, 1, 1e-5, 1e-5, 50, w, &result[i], &error[i]);
    }

    gsl_integration_workspace_free(w);
    }
}
