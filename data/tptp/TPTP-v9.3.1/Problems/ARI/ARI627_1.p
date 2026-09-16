%------------------------------------------------------------------------------
% File     : ARI627_1 : TPTP v9.3.1. Released v6.1.0.
% Domain   : Arithmetic
% Problem  : Overflow checking on the rationals
% Version  : Biased.
% English  : A simple test computing  (2^64-1)/2^64 + (2^64-1)/2^64, for which 
%            the denominator should get too big for machine int, therefore 
%            detecting whether the prover uses arbitrary precision arithmetic.

% Refs     : [Cru14] Cruanes (2014), Email to Geoff Sutcliffe
% Source   : [Cru14]
% Names    :

% Status   : Theorem
% Rating   : 0.20 v9.3.0, 0.25 v9.1.0, 0.38 v9.0.0, 0.25 v8.2.0, 0.38 v7.5.0, 0.40 v7.4.0, 0.50 v7.0.0, 0.57 v6.4.0, 0.33 v6.3.0, 0.57 v6.2.0, 0.62 v6.1.0
% Syntax   : Number of formulae    :    1 (   0 unt;   0 typ;   0 def)
%            Number of atoms       :    2 (   2 equ)
%            Maximal formula atoms :    2 (   2 avg)
%            Number of connectives :    2 (   1   ~;   0   |;   1   &)
%                                         (   0 <=>;   0  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    4 (   4 avg)
%            Maximal term depth    :    2 (   1 avg)
%            Number arithmetic     :    5 (   0 atm;   1 fun;   3 num;   1 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    0 (   0   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    1 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :    3 (   0 usr;   2 con; 0-2 aty)
%            Number of variables   :    1 (   0   !;   1   ?;   1   :)
% SPC      : TF0_THM_EQU_ARI_NDT

% Comments :
%------------------------------------------------------------------------------
tff(the,conjecture,
    ? [X: $rat] :
      ( ( X = $sum(18446744073709551615/18446744073709551616,18446744073709551615/18446744073709551616) )
      & ( X != 2/1 ) ) ).

%------------------------------------------------------------------------------
