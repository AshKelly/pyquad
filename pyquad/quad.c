#include <stdlib.h>
#include <stdio.h>
#include <math.h> // required for fabs()
#include <gsl/gsl_integration.h>
#include <time.h>
#include <omp.h>

typedef double (*integrand)(double, ...);
typedef double (*integrand_wrapper)(double, void *);

typedef struct{
    double * args;
    integrand func;
} params;

static double integrand_0(double x, void * vp){
    params * p = (params *)vp;
    return p->func(x);
}

static double integrand_1(double x, void * vp){
    params * p = (params *)vp;
    return p->func(x, p->args[0]);
}

static double integrand_2(double x, void * vp){
    params * p = (params *)vp;
    return p->func(x, p->args[0], p->args[1]);
}

static double integrand_3(double x, void * vp){
    params * p = (params *)vp;
    return p->func(x, p->args[0], p->args[1], p->args[2]);
}

static double integrand_4(double x, void * vp){
    params * p = (params *)vp;
    return p->func(x, p->args[0], p->args[1], p->args[2], p->args[3]);
}

static double integrand_5(double x, void * vp){
    params * p = (params *)vp;
    return p->func(x, p->args[0], p->args[1], p->args[2], p->args[3], p->args[4]);
}

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

static double integrand_8(double x, void * vp){
    params * p = (params *)vp;
    return p->func(x, p->args[0], p->args[1], p->args[2], p->args[3], p->args[4],
                   p->args[5], p->args[6], p->args[7]);
}

integrand_wrapper select_integrand(int num_args){
    switch(num_args) {
      case 0:
        return integrand_0;
      case 1:
        return integrand_1;
      case 2:
        return integrand_2;
      case 3:
        return integrand_3;
      case 4:
        return integrand_4;
      case 5:
        return integrand_5;
      case 6:
        return integrand_6;
      case 7:
        return integrand_7;
      case 8:
        return integrand_8;
      default:
        return integrand_0;
   }
}

void _quad(int num_args, double a, double b, void * p, double * result, double * error){
    gsl_integration_workspace * w = gsl_integration_workspace_alloc (50);

    gsl_function gfunc;
    gfunc.function = select_integrand(num_args);
    gfunc.params = p;

    gsl_integration_qags(&gfunc, a, b, 1e-7, 1e-7, 50, w, result, error);
    gsl_integration_workspace_free(w);
}

void _quad_grid(int num_args, double a, double b, params ps, int num, double * grid1,
        double * grid2, double * result, double * error){

    // Extend the args array and add the grid args
    double * grid_args = malloc(sizeof(double) * (num_args + 2));
    for(int i=0; i<num_args; i++){
        grid_args[i + 2] = ps.args[i];
    }
    ps.args = &grid_args[0];

    // Set up the integration wroskapce
    gsl_integration_workspace * w = gsl_integration_workspace_alloc(50);
    gsl_function gfunc;
    gfunc.function = select_integrand(num_args + 2);
    gfunc.params = (void *)&ps;

    for(int i=0; i<num; i++){
        ps.args[0] = grid1[i];
        ps.args[1] = grid2[i];
        gsl_integration_qags(&gfunc, a, b, 1e-7, 1e-7, 50, w, &result[i], &error[i]);
    }

    free(grid_args);
    gsl_integration_workspace_free(w);
}

void _quad_grid_parallel(int num_args, double a, double b, params ps, int num,
                         double * grid1, double * grid2, double * result,
                         double * error){
    omp_set_num_threads(8);
    #pragma omp parallel firstprivate(ps) shared(a, b, grid1, grid2, result, error)
    {
    // Extend the args array and add the grid args
    double * grid_args = malloc(sizeof(double) * (num_args + 2));
    for(int i=0; i<num_args; i++){
        grid_args[i + 2] = ps.args[i];
    }
    ps.args = &grid_args[0];

    // Set up the integration wroskapce
    gsl_integration_workspace * w = gsl_integration_workspace_alloc(50);
    gsl_function gfunc;
    gfunc.function = select_integrand(num_args + 2);
    gfunc.params = (void *)&ps;

    #pragma omp for
    for(int i=0; i<num; i++){
        ps.args[0] = grid1[i];
        ps.args[1] = grid2[i];
        gsl_integration_qags(&gfunc, a, b, 1e-7, 1e-7, 50, w, &result[i], &error[i]);
    }

    free(grid_args);
    gsl_integration_workspace_free(w);
    }
}
