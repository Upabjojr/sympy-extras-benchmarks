%------------------------------------------------------------------------------
% File     : ARI579_1 : TPTP v9.3.1. Released v5.1.0.
% Domain   : Arithmetic
% Problem  : Inequation system is not solvable over $int (e.g., X = Y = 1/2)
% Version  : Especial.
% English  :

% Refs     : [Wal10] Waldmann (2010), Email to Geoff Sutcliffe
% Source   : [Wal10]
% Names    :

% Status   : CounterSatisfiable
% Rating   : 0.00 v6.0.0, 0.33 v5.2.0, 1.00 v5.1.0
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
% SPC      : TF0_CSA_NEQ_ARI_NDT

% Comments : A theorem for $rat and $real.
%------------------------------------------------------------------------------
tff(ineq_sys_rat_solvable,conjecture,
    ? [X: $int,Y: $int] :
      ( $less(0,X)
      & $less(0,Y)
      & $less($sum($product(3,X),$product(4,Y)),6) ) ).

%------------------------------------------------------------------------------
