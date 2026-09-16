%------------------------------------------------------------------------------
% File     : ARI579_3 : TPTP v9.3.1. Released v5.1.0.
% Domain   : Arithmetic
% Problem  : Inequation system is solvable over $real (e.g., X = Y = 1/2)
% Version  : Especial.
% English  :

% Refs     : [Wal10] Waldmann (2010), Email to Geoff Sutcliffe
% Source   : [Wal10]
% Names    :

% Status   : Theorem
% Rating   : 0.00 v8.2.0, 0.17 v7.5.0, 0.00 v7.4.0, 0.33 v7.3.0, 0.38 v7.1.0, 0.33 v7.0.0, 0.17 v6.4.0, 0.00 v6.2.0, 0.20 v6.1.0, 0.44 v6.0.0, 0.50 v5.5.0, 0.38 v5.4.0, 0.50 v5.3.0, 0.57 v5.2.0, 0.80 v5.1.0
% Syntax   : Number of formulae    :    1 (   0 unt;   0 typ;   0 def)
%            Number of atoms       :    3 (   0 equ)
%            Maximal formula atoms :    3 (   3 avg)
%            Number of connectives :    2 (   0   ~;   0   |;   2   &)
%                                         (   0 <=>;   0  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    5 (   5 avg)
%            Maximal term depth    :    3 (   1 avg)
%            Number arithmetic     :   13 (   3 atm;   3 fun;   5 num;   2 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    0 (   0   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    1 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :    6 (   0 usr;   4 con; 0-2 aty)
%            Number of variables   :    2 (   0   !;   2   ?;   2   :)
% SPC      : TF0_THM_NEQ_ARI_NDT

% Comments : 
%------------------------------------------------------------------------------
tff(ineq_sys_rat_solvable,conjecture,
    ? [X: $real,Y: $real] :
      ( $less(0.0,X)
      & $less(0.0,Y)
      & $less($sum($product(3.0,X),$product(4.0,Y)),6.0) ) ).

%------------------------------------------------------------------------------
