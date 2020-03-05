#include <stdlib.h>
#include <stdio.h>

#include <math.h>
#include <time.h>

#include "integration/gsl_integration.h"
#include "integration/gsl_errno.h"
#include "integrands.h"

#include <pthread.h>

typedef struct{
    size_t limit;
    params ps;

    int num_grid_args;
    int num_args;

    double * grid;
    double * result;
    double * error;
    int * status;
    double epsabs;
    double epsrel;
    double a;
    double b;

    int upper;
    int lower;
    int integration_method;
} pthread_args;


typedef int (integrator)(const gsl_function *, double, double, double, double, size_t, void *,
        double *, double *);


void * allocate_workspace(int integration_type, size_t limit){
    if (integration_type == 0){
        return gsl_integration_workspace_alloc(limit);
    }
    else if (integration_type == 1){
        return gsl_integration_cquad_workspace_alloc(limit);
    }
    else{
        exit(1);
    }
}


void deallocate_workspace(int integration_type, void * w){
    if (integration_type == 0){
        gsl_integration_workspace_free(w);
    }
    else if (integration_type == 1){
        gsl_integration_cquad_workspace_free(w);
    }
    else{
        exit(1);
    }
}


integrator * select_integration_func(int integration_type){
    if (integration_type == 0){
        return &gsl_integration_qags;
    }
    else if (integration_type == 1){
        return &gsl_integration_cquad;
    }
    else{
        exit(1);
    }
}


void _quad(int num_args, double a, double b, void * p, double epsabs,
    double epsrel, size_t limit, double * result, double * error, int * status,
    int integration_method){

    void * w = allocate_workspace(integration_method, limit);
    integrator * func = select_integration_func(integration_method);

    gsl_function gfunc;
    gfunc.function = integrand_functions[num_args][0];
    gfunc.params = p;

    (*status) = (*func)(
            &gfunc, a, b, epsabs, epsrel, limit, w, result, error
            );

    deallocate_workspace(integration_method, w);
}


void _quad_grid(int num_args, int num_grid_args, double a, double b, params ps,
    int num, double epsabs, double epsrel, size_t limit, double * grid,
    double * result, double * error, int * status, int integration_method){

    // Set up the integration workspace
    void * w = allocate_workspace(integration_method, limit);
    integrator * func = select_integration_func(integration_method);

    gsl_function gfunc;
    gfunc.function = integrand_functions[num_args][num_grid_args];
    gfunc.params = (void *)&ps;

    for(int i=0; i<num; i++){
        ps.grid_args = &grid[i*num_grid_args];
        status[i] = (*func)(&gfunc, a, b, epsabs, epsrel, limit, w,
                             &result[i], &error[i]);
    }

    deallocate_workspace(integration_method, w);
}


void * _quad_grid_parallel(void * args){
    pthread_args * pargs = (pthread_args *) args;

    void * w = allocate_workspace(pargs->integration_method, pargs->limit);
    integrator * func = select_integration_func(pargs->integration_method);

    // deactivate default gsl error handler
    gsl_function gfunc;
    gfunc.function = integrand_functions[pargs->num_args][pargs->num_grid_args];
    gfunc.params = (void *)&pargs->ps;
    for(int i=pargs->lower; i<pargs->upper; i++){
        pargs->ps.grid_args = &pargs->grid[i * pargs->num_grid_args];

        pargs->status[i] = (*func)(&gfunc, pargs->a, pargs->b, pargs->epsabs,
                             pargs->epsrel, pargs->limit, w, &pargs->result[i],
                             &pargs->error[i]);
    }
    deallocate_workspace(pargs->integration_method, w);

    return NULL;
}

void _quad_grid_parallel_wrapper(int num_args, int num_grid_args, double a,
    double b, params ps, int num, double epsabs, double epsrel, size_t limit,
    double * grid, double * result, double * error, int num_threads,
    int pin_threads, int * status, int integration_method){

    int num_per_thread = num / num_threads;
    pthread_args pargs[num_threads];
    pthread_t thread[num_threads];

    pthread_attr_t attr;
    pthread_attr_init(&attr);

    #ifdef LINUX_MACH
    cpu_set_t cpus;
    #endif

    for(int i=0; i < num_threads; i++){
        // Pass the relevant work
        pargs[i].num_args = num_args;
        pargs[i].num_grid_args = num_grid_args;
        pargs[i].grid = grid;
        pargs[i].limit = limit;
        pargs[i].ps = ps;
        pargs[i].result = result;
        pargs[i].error = error;
        pargs[i].a = a;
        pargs[i].b = b;
        pargs[i].epsabs = epsabs;
        pargs[i].epsrel = epsrel;
	    pargs[i].status = status;
        pargs[i].integration_method = integration_method;

        // Get the range of integrals for this thread
        pargs[i].lower = num_per_thread * i;
        pargs[i].upper = num_per_thread * (i + 1);

        // Just ensure there are no uncalculated integrals
        if(i == (num_threads - 1)){
            pargs[i].upper = num;
        }

        // Pin each thread to an individual core
        #ifdef LINUX_MACH
        if (pin_threads == 1){
            CPU_ZERO(&cpus);
            CPU_SET(i, &cpus);
            pthread_attr_setaffinity_np(&attr, sizeof(cpu_set_t), &cpus);
        }
        #endif

        pthread_create(&thread[i], &attr, _quad_grid_parallel, (void *) &pargs[i]);
    }

    for(int i=0; i < num_threads; i++){
        pthread_join(thread[i], NULL);
    }
}
