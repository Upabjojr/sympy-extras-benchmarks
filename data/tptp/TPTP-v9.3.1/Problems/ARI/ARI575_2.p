%------------------------------------------------------------------------------
% File     : ARI575_2 : TPTP v9.3.1. Released v5.1.0.
% Domain   : Arithmetic
% Problem  : Inequation system has more than one rational solution
% Version  : Especial.
% English  :

% Refs     : [Wal10] Waldmann (2010), Email to Geoff Sutcliffe
% Source   : [Wal10]
% Names    :

% Status   : CounterSatisfiable
% Rating   : 0.33 v7.1.0, 0.50 v7.0.0, 0.67 v6.4.0, 0.33 v6.0.0, 0.50 v5.4.0, 0.00 v5.3.0, 0.33 v5.2.0, 1.00 v5.1.0
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
% SPC      : TF0_CSA_EQU_ARI_NDT

% Comments : 
%------------------------------------------------------------------------------
tff(ineq_sys_has_1_int_sol,conjecture,
    ! [X: $rat,Y: $rat,Z: $rat] :
      ( ( $less(3/1,X)
        & $less(X,Y)
        & $less(Y,Z)
        & $less($sum($sum(X,$product(2/1,Y)),$product(3/1,Z)),35/1) )
    <=> ( ( X = 4/1 )
        & ( Y = 5/1 )
        & ( Z = 6/1 ) ) ) ).

%------------------------------------------------------------------------------
