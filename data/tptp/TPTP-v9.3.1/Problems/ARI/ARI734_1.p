%------------------------------------------------------------------------------
% File     : ARI734_1 : TPTP v9.3.1. Released v6.4.0.
% Domain   : Arithmetic
% Problem  : Verification example
% Version  : Especial.
% English  :

% Refs     : [Bau15a] Baumgartner (2015), Email to Geoff Sutcliffe
%          : [Bau15b] Baumgartner (2015), SMTtoTPTP - A Converter for Theore
% Source   : [Bau15a]
% Names    : swv-double-1.p [Bau15a]

% Status   : Theorem
% Rating   : 0.00 v9.3.0, 0.12 v7.5.0, 0.20 v7.4.0, 0.12 v7.3.0, 0.17 v7.0.0, 0.00 v6.4.0
% Syntax   : Number of formulae    :    1 (   0 unt;   0 typ;   0 def)
%            Number of atoms       :    8 (   7 equ)
%            Maximal formula atoms :    8 (   8 avg)
%            Number of connectives :    8 (   1   ~;   0   |;   4   &)
%                                         (   0 <=>;   3  =>;   0  <=;   0 <~>)
%            Maximal formula depth :   10 (  10 avg)
%            Maximal term depth    :    2 (   1 avg)
%            Number arithmetic     :   17 (   1 atm;   4 fun;   8 num;   4 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    0 (   0   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    2 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :    6 (   0 usr;   3 con; 0-2 aty)
%            Number of variables   :    4 (   1   !;   3   ?;   4   :)
% SPC      : TF0_THM_EQU_ARI_NDT

% Comments : Converted from SMT using [Bau15b]
%------------------------------------------------------------------------------
tff(formula,conjecture,
    ! [I: $int] :
      ( $greatereq(I,0)
     => ? [Res_1: $int] :
          ( ? [Res1_2: $int] :
              ( ? [I_3: $int] :
                  ( ( I_3 = $difference(I,1) )
                  & ( Res1_2 = $product(2,I_3) ) )
              & ( ( I = 0 )
               => ( Res_1 = 0 ) )
              & ( ( I != 0 )
               => ( Res_1 = $sum(Res1_2,2) ) ) )
          & ( Res_1 = $product(2,I) ) ) ) ).

%------------------------------------------------------------------------------
