%------------------------------------------------------------------------------
% File     : ARI127_1 : TPTP v9.3.1. Released v5.0.0.
% Domain   : Arithmetic
% Problem  : Integer: Not product of only 2 and only 4 is 8
% Version  : Especial.
% English  :

% Refs     :
% Source   : [TPTP]
% Names    :

% Status   : CounterSatisfiable
% Rating   : 0.00 v8.2.0, 0.33 v8.1.0, 0.00 v7.3.0, 0.33 v7.1.0, 0.50 v7.0.0, 0.33 v6.4.0, 0.67 v6.3.0, 0.33 v6.2.0, 0.00 v6.0.0, 0.50 v5.4.0, 0.33 v5.2.0, 1.00 v5.0.0
% Syntax   : Number of formulae    :    1 (   0 unt;   0 typ;   0 def)
%            Number of atoms       :    3 (   3 equ)
%            Maximal formula atoms :    3 (   3 avg)
%            Number of connectives :    2 (   0   ~;   0   |;   1   &)
%                                         (   0 <=>;   1  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    5 (   5 avg)
%            Maximal term depth    :    2 (   1 avg)
%            Number arithmetic     :    6 (   0 atm;   1 fun;   3 num;   2 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    0 (   0   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    1 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :    4 (   0 usr;   3 con; 0-2 aty)
%            Number of variables   :    2 (   2   !;   0   ?;   2   :)
% SPC      : TF0_CSA_EQU_ARI_NDT

% Comments :
%------------------------------------------------------------------------------
tff(anti_product_only_2_only_4_8,conjecture,
    ! [X: $int,Y: $int] :
      ( ( $product(X,Y) = 8 )
     => ( ( X = 2 )
        & ( Y = 4 ) ) ) ).

%------------------------------------------------------------------------------
