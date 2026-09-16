%------------------------------------------------------------------------------
% File     : ARI575_1 : TPTP v9.3.1. Released v5.1.0.
% Domain   : Arithmetic
% Problem  : Inequation system has exactly one integer solution
% Version  : Especial.
% English  :

% Refs     : [Wal10] Waldmann (2010), Email to Geoff Sutcliffe
% Source   : [Wal10]
% Names    :

% Status   : Theorem
% Rating   : 0.00 v9.3.0, 0.12 v9.1.0, 0.25 v9.0.0, 0.12 v7.5.0, 0.10 v7.4.0, 0.12 v7.3.0, 0.17 v7.0.0, 0.00 v6.3.0, 0.29 v6.2.0, 0.38 v6.1.0, 0.44 v6.0.0, 0.43 v5.5.0, 0.56 v5.4.0, 0.50 v5.2.0, 0.83 v5.1.0
% Syntax   : Number of formulae    :    1 (   0 unt;   0 typ;   0 def)
%            Number of atoms       :    7 (   3 equ)
%            Maximal formula atoms :    7 (   7 avg)
%            Number of connectives :    6 (   0   ~;   0   |;   5   &)
%                                         (   1 <=>;   0  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    8 (   8 avg)
%            Maximal term depth    :    4 (   1 avg)
%            Number arithmetic     :   18 (   4 atm;   4 fun;   7 num;   3 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    0 (   0   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    2 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :    8 (   0 usr;   6 con; 0-2 aty)
%            Number of variables   :    3 (   3   !;   0   ?;   3   :)
% SPC      : TF0_THM_EQU_ARI_NDT

% Comments : Countersatisfiable for $rat, $real
%------------------------------------------------------------------------------
tff(ineq_sys_has_1_int_sol,conjecture,
    ! [X: $int,Y: $int,Z: $int] :
      ( ( $less(3,X)
        & $less(X,Y)
        & $less(Y,Z)
        & $less($sum($sum(X,$product(2,Y)),$product(3,Z)),35) )
    <=> ( ( X = 4 )
        & ( Y = 5 )
        & ( Z = 6 ) ) ) ).

%------------------------------------------------------------------------------
