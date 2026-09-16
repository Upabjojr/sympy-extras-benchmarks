%------------------------------------------------------------------------------
% File     : ARI735_1 : TPTP v9.3.1. Released v6.4.0.
% Domain   : Arithmetic
% Problem  : Verification example
% Version  : Especial.
% English  :

% Refs     : [Bau15a] Baumgartner (2015), Email to Geoff Sutcliffe
%          : [Bau15b] Baumgartner (2015), SMTtoTPTP - A Converter for Theore
% Source   : [Bau15a]
% Names    : swv-double-2.p [Bau15a]

% Status   : Theorem
% Rating   : 0.00 v9.3.0, 0.12 v7.5.0, 0.20 v7.4.0, 0.12 v7.3.0, 0.17 v7.0.0, 0.00 v6.4.0
% Syntax   : Number of formulae    :    1 (   0 unt;   0 typ;   0 def)
%            Number of atoms       :    6 (   3 equ)
%            Maximal formula atoms :    6 (   6 avg)
%            Number of connectives :    6 (   1   ~;   0   |;   2   &)
%                                         (   0 <=>;   3  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    7 (   7 avg)
%            Maximal term depth    :    2 (   1 avg)
%            Number arithmetic     :   10 (   2 atm;   1 fun;   5 num;   2 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    0 (   0   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    3 (   0 usr;   1 prp; 0-2 aty)
%            Number of functors    :    3 (   0 usr;   2 con; 0-2 aty)
%            Number of variables   :    2 (   1   !;   1   ?;   2   :)
% SPC      : TF0_THM_EQU_ARI_NDT

% Comments : Converted from SMT using [Bau15b]
%------------------------------------------------------------------------------
tff(formula,conjecture,
    ! [I: $int] :
      ( $greatereq(I,0)
     => ( ( ( I = 0 )
         => $true )
        & ( ( I != 0 )
         => ? [I_1: $int] :
              ( ( I_1 = $difference(I,1) )
              & $greatereq(I_1,0) ) ) ) ) ).

%------------------------------------------------------------------------------
