%------------------------------------------------------------------------------
% File     : ARI624_1 : TPTP v9.3.1. Bugfixed v5.2.0.
% Domain   : Arithmetic
% Problem  : f(X) cannot always be smaller than avg(f(X-Y),f(X+Y)) - 1
% Version  : Especial.
% English  :

% Refs     : [Wal10] Waldmann (2010), Email to Geoff Sutcliffe
% Source   : [Wal10]
% Names    :

% Status   : Theorem
% Rating   : 1.00 v5.2.0
% Syntax   : Number of formulae    :    2 (   0 unt;   1 typ;   0 def)
%            Number of atoms       :    2 (   0 equ)
%            Maximal formula atoms :    2 (   2 avg)
%            Number of connectives :    2 (   1   ~;   0   |;   0   &)
%                                         (   0 <=>;   1  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    5 (   5 avg)
%            Maximal term depth    :    7 (   2 avg)
%            Number arithmetic     :   15 (   2 atm;   7 fun;   4 num;   2 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    1 (   1   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    2 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :    7 (   1 usr;   3 con; 0-2 aty)
%            Number of variables   :    2 (   2   !;   0   ?;   2   :)
% SPC      : TF0_THM_NEQ_ARI_NDT

% Comments : Also a theorem for $real
% Bugfixes : v5.2.0 - Made numbers into rationals.
%------------------------------------------------------------------------------
tff(f_type,type,
    f: $rat > $rat ).

tff(not_ex_f_smaller_avg_minus_1,conjecture,
    ~ ! [X: $rat,Y: $rat] :
        ( $greater(Y,0/1)
       => $less(f(X),$sum($sum($product(1/2,f($sum(X,$uminus(Y)))),$product(1/2,f($sum(X,Y)))),-1/1)) ) ).

%------------------------------------------------------------------------------
