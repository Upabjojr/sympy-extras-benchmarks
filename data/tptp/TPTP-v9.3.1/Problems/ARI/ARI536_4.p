%------------------------------------------------------------------------------
% File     : ARI536_4 : TPTP v9.3.1. Released v5.3.0.
% Domain   : Arithmetic
% Problem  : Rational: Square root of two does not exist
% Version  : Especial.
% English  : 

% Refs     : [SB+03] Siekman et al. (2003), Proof Development with Omega: T
% Source   : [TPTP]
% Names    :

% Status   : CounterSatisfiable
% Rating   : 0.67 v8.2.0, 1.00 v6.3.0, 0.67 v6.2.0, 0.33 v6.0.0, 0.75 v5.4.0, 0.67 v5.3.0
% Syntax   : Number of formulae    :    1 (   1 unt;   0 typ;   0 def)
%            Number of atoms       :    1 (   1 equ)
%            Maximal formula atoms :    1 (   1 avg)
%            Number of connectives :    0 (   0   ~;   0   |;   0   &)
%                                         (   0 <=>;   0  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    2 (   2 avg)
%            Maximal term depth    :    2 (   1 avg)
%            Number arithmetic     :    3 (   0 atm;   1 fun;   1 num;   1 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    0 (   0   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    1 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :    2 (   0 usr;   1 con; 0-2 aty)
%            Number of variables   :    1 (   0   !;   1   ?;   1   :)
% SPC      : TF0_CSA_EQU_ARI_NDT

% Comments : 
%------------------------------------------------------------------------------
tff(the,conjecture,
    ? [X: $rat] : ( $product(X,X) = 2/1 ) ).

%------------------------------------------------------------------------------
