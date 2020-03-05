/* sys/infnan.c
 *
 * Copyright (C) 2001, 2004, 2007, 2010 Brian Gough
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3 of the License, or (at
 * your option) any later version.
 *
 * This program is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301,
 * USA.
 */
#ifndef __GSL_INFNNA__
#define __GSL_INFNAN__

#include <math.h>
#define HAVE_DECL_FINITE 1
#define HAVE_DECL_ISNAN 1
#include <float.h>
//#include "ieeefp.h"
//#include "fdiv.c"

#include "gsl_sys.h"

double gsl_nan(void) { return gsl_fdiv(0.0, 0.0); }

double gsl_posinf(void) { return gsl_fdiv(+1.0, 0.0); }

double gsl_neginf(void) { return gsl_fdiv(-1.0, 0.0); }

// int gsl_isnan (const double x);
// int gsl_isinf (const double x);
// int gsl_finite (const double x);

int gsl_finite(const double x) {
    const double y = x - x;
    int status = (y == y);
    return status;
}

int gsl_isnan(const double x) {
    int status = (x != x);
    return status;
}

int gsl_isinf(const double x) {
    /* isinf(3): In glibc 2.01 and earlier, isinf() returns a
       non-zero value (actually: 1) if x is an infinity (positive or
       negative).  (This is all that C99 requires.) */

    if (isinf(x)) {
        return (x > 0) ? 1 : -1;
    } else {
        return 0;
    }
}

#endif
