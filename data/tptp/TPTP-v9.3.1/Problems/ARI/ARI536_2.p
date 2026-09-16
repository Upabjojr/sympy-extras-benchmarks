%------------------------------------------------------------------------------
% File     : ARI536_2 : TPTP v9.3.1. Released v5.0.0.
% Domain   : Arithmetic
% Problem  : Real: Square root of two exists and is not rational
% Version  : Especial.
% English  : 

% Refs     : [SB+03] Siekman et al. (2003), Proof Development with Omega: T
% Source   : [TPTP]
% Names    :

% Status   : Theorem
% Rating   : 0.80 v9.3.0, 0.88 v9.0.0, 0.75 v8.2.0, 0.88 v8.1.0, 1.00 v7.0.0, 0.86 v6.4.0, 0.67 v6.3.0, 0.86 v6.2.0, 1.00 v6.1.0, 0.89 v6.0.0, 0.86 v5.5.0, 0.89 v5.4.0, 0.88 v5.3.0, 0.90 v5.2.0, 1.00 v5.0.0
% Syntax   : Number of formulae    :    1 (   0 unt;   0 typ;   0 def)
%            Number of atoms       :    2 (   1 equ)
%            Maximal formula atoms :    2 (   2 avg)
%            Number of connectives :    2 (   1   ~;   0   |;   0   &)
%                                         (   0 <=>;   1  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    4 (   4 avg)
%            Maximal term depth    :    2 (   1 avg)
%            Number arithmetic     :    4 (   1 atm;   1 fun;   1 num;   1 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    0 (   0   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    2 (   0 usr;   0 prp; 1-2 aty)
%            Number of functors    :    2 (   0 usr;   1 con; 0-2 aty)
%            Number of variables   :    1 (   1   !;   0   ?;   1   :)
% SPC      : TF0_THM_EQU_ARI_NDT

% Comments : 
%------------------------------------------------------------------------------
tff(the,conjecture,
    ! [X: $real] :
      ( ( $product(X,X) = 2.0 )
     => ~ $is_rat(X) ) ).

%------------------------------------------------------------------------------
